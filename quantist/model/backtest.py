from typing import List

import pandas as pd

from provider.handler import DynamoDBHandler
from provider.manager import get_price_by_entire
from utils import convert_dt


class BacktestRunner(object):
    def __init__(self, model):
        self.model = model
        self.portfolio = model.portfolio
        self.positions = dict(buy=[], sell=[])
        self.start = convert_dt(2017, 9, 1)
        self.end = convert_dt(2018, 5, 10)
        self.slippage = 0
        self.entire = False

    def initialize(self, start_date: str, end_date: str, entire: bool):
        self.start = start_date
        self.end = end_date
        self.entire = entire

    def load_data(self, stock: str) -> List[dict]:
        db = DynamoDBHandler('stock')
        return db.get_price_by_date(stock, self.start, self.end) \
            if self.entire is False else get_price_by_entire(stock, self.start, self.end)

    def load_baseline(self, baseline: str) -> List[dict]:
        db = DynamoDBHandler('index')
        return db.get_baseline(baseline, self.start, self.end)

    def order_price(self, price, way: str):
        self.positions[way.lower()].append(price)

    def backtest(self, start_date: str, end_date: str, baseline: str, entire: bool):
        self.initialize(start_date, end_date, entire)
        records = []
        daily_port = []
        for stock, ratio in self.portfolio.ratio.items():
            self.positions = dict(buy=[], sell=[])
            items = self.load_data(stock)

            # Create DataFrame
            df = pd.DataFrame(items, columns=['name', 'date', 'close', 'diff'])
            df['close'] = df.close.astype(int)
            df = df.set_index('date').sort_index()
            first_price = int(df['close'][0])

            self.model.handle_data(df)
            seed = int(self.portfolio.cash * ratio)
            for buy, sell in zip(self.positions['buy'], self.positions['sell']):
                profit = self.portfolio.calculate_profit(seed, buy, sell)
                holding = seed - self.portfolio.buy_price(seed, buy)[1]
                profit_rate = round((profit / seed) * 100, 2)
                records.append((stock, ratio, seed, profit, holding, profit_rate))
                seed += profit

            # Make daily profit change DF
            result = df.close.apply(
                lambda x: self.portfolio.profit_ratio(first_price, x))
            daily_port.append(result)

        # Portfolio report
        df = pd.concat(daily_port, axis=1, keys=self.portfolio.ratio.keys())
        bs = pd.DataFrame(
            self.load_baseline(baseline), columns=['name', 'date', 'price'])
        self.portfolio.report(df, bs, records)
