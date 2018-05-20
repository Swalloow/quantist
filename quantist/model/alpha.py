from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from portfolio.builder import Portfolio
from provider.handler import DynamoDBHandler
from provider.manager import get_price_by_entire


class AbstractModel(ABC):
    def __init__(self, cash: int=10000000):
        self.stock = []
        self.ratio = []
        self.indicators = {}
        self.portfolio = Portfolio(cash)

    @abstractmethod
    def initialize(self):
        raise NotImplementedError('Not implemented')

    @abstractmethod
    def handle_data(self):
        raise NotImplementedError('Not implemented')

    def backtest(self, start_date: str, end_date: str, entire: bool=False):
        self.initialize()
        db = DynamoDBHandler('stock')

        records = []
        daily_port = []
        for stock, ratio in self.portfolio.ratio.items():
            items = db.get_price_by_date(stock, start_date, end_date) if entire is False \
                else get_price_by_entire(stock, start_date, end_date)
            seed = int(self.portfolio.cash * ratio)
            buy = int(items[0]['close'])
            sell = int(items[-1]['close'])
            profit = self.portfolio.calculate_profit(seed, buy, sell)
            holding = seed - self.portfolio.buy_price(seed, buy)[1]
            profit_rate = round((profit / seed) * 100, 2)
            records.append((stock, ratio, seed, profit, holding, profit_rate))

            # Make daily profit change DF
            df = pd.DataFrame(items, columns=['name', 'date', 'close', 'diff'])
            df['close'] = df.close.astype(int)
            df = df.set_index('date').sort_index()
            result = df.close.apply(lambda x: self.portfolio.profit_ratio(buy, x))
            daily_port.append(result)

        # Portfolio mean-variance
        df = pd.concat(daily_port, axis=1, keys=self.portfolio.ratio.keys())
        w = np.array(list(self.portfolio.ratio.values())).T
        mean, var = self.portfolio.calculate_mean_var(df.mean(), df.corr(), w)

        # Make report DF
        col = ['stock', 'ratio', 'seed', 'profit', 'holding', 'profit_rate']
        report = pd.DataFrame.from_records(records, columns=col)
        total_profit = sum(report.profit.tolist())
        total_profit_rate = round((total_profit / self.portfolio.cash) * 100, 2)

        print("-----------------------------------------------")
        print("total profit: {} / {}%".format(total_profit, total_profit_rate))
        print("portfolio mean: {}".format(mean))
        print("portfolio variance: {}".format(var))
        print(report)
        self.portfolio.plot_profit_change(df)
