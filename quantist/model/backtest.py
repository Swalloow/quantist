from provider.handler import DynamoDBHandler
from provider.manager import get_price_by_entire
import pandas as pd


class BacktestRunner(object):
    def __init__(self, model):
        self.db = DynamoDBHandler('stock')
        self.model = model
        self.portfolio = model.portfolio
        self.slippage = 0   # TODO: Add slippage model
        self.entire = False

    def load_data(self, stock: str, start_date: str, end_date: str):
        return self.db.get_price_by_date(stock, start_date, end_date) \
            if self.entire is False else get_price_by_entire(stock, start_date, end_date)

    def backtest(self, start_date: str, end_date: str, entire: bool=False):
        records = []
        daily_port = []
        for stock, ratio in self.portfolio.ratio.items():
            items = self.load_data(stock, start_date, end_date)

            # Create DataFrame
            df = pd.DataFrame(items, columns=['name', 'date', 'close', 'diff'])
            df['close'] = df.close.astype(int)
            df = df.set_index('date').sort_index()

            # TODO: Apply seasonal strategy
            buy, sell = self.model.handle_data(df)
            seed = int(self.portfolio.cash * ratio)
            profit = self.portfolio.calculate_profit(seed, buy, sell)
            holding = seed - self.portfolio.buy_price(seed, buy)[1]
            profit_rate = round((profit / seed) * 100, 2)
            records.append((stock, ratio, seed, profit, holding, profit_rate))

            # Make daily profit change DF
            result = df.close.apply(lambda x: self.portfolio.profit_ratio(buy, x))
            daily_port.append(result)

            # Portfolio report
        df = pd.concat(daily_port, axis=1, keys=self.portfolio.ratio.keys())
        self.portfolio.report(df, records)
