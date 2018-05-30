from model.alpha import AbstractModel
from utils import convert_dt


class SeasonalModel(AbstractModel):
    def initialize(self):
        self.stock = ['044340', '017670']   # WINIX, SKT
        self.ratio = [1.0, 1.0]
        self.indicators = {}
        self.portfolio.update(self.stock, self.ratio)

    # Implement your logic here
    def handle_data(self, df):
        if df['name'][0] == '044340':   # If WINIX
            buy_price = df[df.index.str.contains('-02-01')]['close'].tolist()
            sell_price = df[df.index.str.contains('-04-03')]['close'].tolist()
            for buy, sell in zip(buy_price, sell_price):
                self.runner.order_price(int(buy), 'buy')
                self.runner.order_price(int(sell), 'sell')

        if df['name'][0] == '017670':   # If SKT
            buy_price = df[df.index.str.contains('-11-10')]['close'].tolist()
            sell_price = df[df.index.str.contains('-12-11')]['close'].tolist()
            for buy, sell in zip(buy_price, sell_price):
                self.runner.order_price(int(buy), 'buy')
                self.runner.order_price(int(sell), 'sell')


if __name__ == '__main__':
    model = SeasonalModel(cash=10000000)
    start_date = convert_dt(2017, 1, 1)
    end_date = convert_dt(2018, 5, 1)
    model.run(start_date, end_date, entire=True, baseline='KOSPI')
