from abc import ABC, abstractmethod
from portfolio.builder import Portfolio
from provider.handler import DynamoDBHandler
from utils import buy_price, sell_price


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
        print(start_date, end_date, self.portfolio.cash, sep=', ')
        db = DynamoDBHandler('stock')

        total = []
        for stock, ratio in self.portfolio.ratio.items():
            seed = self.portfolio.cash * ratio
            res = db.get_price_by_date(stock, start_date, end_date)
            cnt, buy = buy_price(seed, int(res[0]['close']))
            sell = sell_price(cnt, int(res[-1]['close']))
            print(stock, ratio, buy, sell, sell - buy, sep=', ')
            total.append(sell - buy)
        print(sum(total))
