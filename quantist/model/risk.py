import numpy as np


class MarkowitzModel(object):
    def __init__(self, stock):
        self.stock = stock
        self.ratio = []

    def optimize(self):
        # TODO: Apply markowitz model
        k = np.random.rand(len(self.stock))
        return k / sum(k)
