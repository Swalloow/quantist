from model.alpha import AbstractAlphaModel
from utils import convert_dt


class BuyAndHoldModel(AbstractAlphaModel):
    def init(self):
        self.indicators = {}
        self.handle_data()

    def handle_data(self):
        # implement logic
        stock = ['035420', '035720', '068270', '096770']
        ratio = [0.3, 0.3, 0.2, 0.2]
        self.portfolio.update(10000000, stock, ratio)


if __name__ == '__main__':
    model = BuyAndHoldModel()
    model.init()
    start_date = convert_dt(2017, 10, 1)
    end_date = convert_dt(2018, 2, 1)
    model.backtest(start_date, end_date)
