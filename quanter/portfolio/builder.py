class Portfolio(object):
    def __init__(self, cash: float, ratio: dict=None):
        self.cash = cash
        self.ratio = {} if ratio is None else ratio

    def update(self, cash: float, stock: list, weight: list):
        self.cash = cash
        self.ratio = dict(zip(stock, weight))

    def __str__(self):
        return "cash: {}\nratio: {}".format(self.cash, self.ratio)
