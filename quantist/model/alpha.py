from abc import ABC, abstractmethod

from backtest import BacktestRunner
from portfolio.builder import Portfolio


class AbstractModel(ABC):
    def __init__(self, cash: int = 10000000):
        self.stock = []
        self.ratio = []
        self.indicators = {}
        self.portfolio = Portfolio(cash)
        self.environment = BacktestRunner(self)

    @abstractmethod
    def initialize(self):
        """Initialize portfolio"""
        raise NotImplementedError('Not implemented')

    @abstractmethod
    def handle_data(self, data):
        """
        Handling time series data for order price
        """
        raise NotImplementedError('Not implemented')

    def run(self, start_date: str, end_date: str, entire: bool=False):
        self.initialize()
        self.environment.backtest(start_date, end_date, entire)
