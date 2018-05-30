from abc import ABC, abstractmethod

from backtest import BacktestRunner
from portfolio.builder import Portfolio


class AbstractModel(ABC):
    def __init__(self, cash: int = 10000000):
        self.stock = []
        self.ratio = []
        self.indicators = {}  # TODO: Add indicator
        self.portfolio = Portfolio(cash)
        self.runner = BacktestRunner(self)

    @abstractmethod
    def initialize(self):
        """Initialize portfolio"""
        raise NotImplementedError('Not implemented')

    @abstractmethod
    def handle_data(self, data):
        """Handling time series data for order price"""
        raise NotImplementedError('Not implemented')

    def run(self, start_date: str, end_date: str, baseline: str = 'KOSPI',
            entire: bool = False):
        """Run backtest environment with initialize"""
        self.initialize()
        self.runner.backtest(start_date, end_date, baseline, entire)
