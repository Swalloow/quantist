from abc import ABC, abstractmethod
from portfolio.builder import Portfolio


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
        print("{}, {}".format(start_date, end_date))
        print(self.portfolio)
