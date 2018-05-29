from model.alpha import AbstractModel
from utils import convert_dt


class SeasonalModel(AbstractModel):
    def initialize(self):
        self.stock = ['044340', '017670']
        self.ratio = [1.0, 1.0]
        self.indicators = {}
        self.portfolio.update(self.stock, self.ratio)

    # Implement your logic here
    def handle_data(self, data):
        # TODO: Add order price with date value
        buy = int(data['close'][0])
        sell = int(data['close'][-1])
        return buy, sell


if __name__ == '__main__':
    model = SeasonalModel(cash=10000000)
    start_date = convert_dt(2017, 1, 1)
    end_date = convert_dt(2018, 5, 1)
    model.run(start_date, end_date, entire=True)
