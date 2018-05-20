from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from portfolio.builder import Portfolio
from provider.handler import DynamoDBHandler


class AbstractAlphaModel(ABC):
    def __init__(self):
        self.indicators = {}
        self.portfolio = Portfolio(1000000.0)

    @abstractmethod
    def init(self):
        raise NotImplementedError('Not implemented')

    @abstractmethod
    def handle_data(self):
        raise NotImplementedError('Not implemented')

    def backtest(self, start_date, end_date):
        print(self.portfolio)
        db = DynamoDBHandler('stock')

        total = []
        dfs = []
        for stock, ratio in self.portfolio.ratio.items():
            seed = self.portfolio.cash * ratio
            items = db.get_price_by_date(stock, start_date, end_date)
            buy = int(items[0]['close'])
            sell = int(items[-1]['close'])

            # Calculate exp, risk
            df = pd.DataFrame(items, columns=['name', 'date', 'close', 'diff'])
            result = df.close.apply(lambda x: self.portfolio.profit_ratio(buy, x))
            dfs.append(result)

            # Prev
            profit = self.portfolio.calculate_profit(seed, buy, sell)
            total.append(profit)
            # self.portfolio.plot_profit_change(items, buy)

        print("profit: {}".format(sum(total)))
        df = pd.concat(dfs, axis=1, keys=self.portfolio.ratio.keys())
        avg_ret = df.mean()
        var_covar = df.cov()

        w = np.array(list(self.portfolio.ratio.values())).T
        mean, var = self.portfolio.port_mean_var(avg_ret, var_covar, w)

        print("Mean of portfolio: {}".format(mean))
        print("Varience of portfolio: {}".format(var))
