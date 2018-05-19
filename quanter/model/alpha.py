from abc import ABC, abstractmethod

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
        for stock, ratio in self.portfolio.ratio.items():
            seed = self.portfolio.cash * ratio
            items = db.get_price_by_date(stock, start_date, end_date)
            buy = int(items[0]['close'])
            sell = int(items[-1]['close'])
            profit = self.portfolio.calculate_profit(seed, buy, sell)
            total.append(profit)
            self.portfolio.plot_profit_change(buy, items)

        print("profit: {}".format(sum(total)))
