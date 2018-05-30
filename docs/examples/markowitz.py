from model.alpha import AbstractModel
from utils import convert_dt
from model.risk import MarkowitzModel


class BuyAndHoldOptModel(AbstractModel):
    def initialize(self):
        # NAVER, KAKAO, CELLTRION, SKINNO
        self.stock = ['035420', '035720', '068270', '096770']
        self.ratio = MarkowitzModel(self.stock).optimize()
        self.indicators = {}
        self.portfolio.update(self.stock, self.ratio)

    # Implement your logic here
    def handle_data(self, df):
        self.runner.order_price(int(df['close'][0]), 'buy')
        self.runner.order_price(int(df['close'][-1]), 'sell')


if __name__ == '__main__':
    model = BuyAndHoldOptModel(cash=10000000)
    start_date = convert_dt(2017, 12, 1)
    end_date = convert_dt(2018, 2, 1)
    model.run(start_date, end_date, baseline='KOSPI')
