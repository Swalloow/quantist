from math import trunc
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_style('darkgrid')


class Portfolio(object):
    def __init__(self, cash: float, ratio: dict=None):
        self.cash = cash
        self.ratio = {} if ratio is None else ratio

    def update(self, cash: float, stock: list, weight: list):
        self.cash = cash
        self.ratio = dict(zip(stock, weight))

    def calculate_profit(self, cash: int, buy: int, sell: int) -> int:
        cnt, buy = self.buy_price(cash, buy)
        sell = self.sell_price(cnt, sell)
        return sell - buy

    def calculate_exp(self):
        raise NotImplementedError('TODO')

    def calculate_risk(self):
        raise NotImplementedError('TODO')

    @staticmethod
    def buy_price(cash: int, price: int) -> (int, int):
        return trunc(cash / price), trunc(cash / price) * price

    @staticmethod
    def sell_price(count: int, price: int) -> int:
        return count * price

    @staticmethod
    def profit_ratio(buy: int, sell: int):
        return round((sell - buy) / sell * 100, 2)

    @staticmethod
    def port_mean_var(avg_ret_, var_covar_, w_):
        port_ret = np.dot(w_, avg_ret_)
        port_std = np.dot(np.dot(w_, var_covar_), w_.T)
        return port_ret, port_std

    def plot_profit_change(self, items: List[dict], buy: int):
        df = pd.DataFrame(items, columns=['name', 'date', 'close', 'diff'])
        rate = df.close.apply(lambda x: self.profit_ratio(buy, x)).tolist()
        plt.title("{} profit change".format(df.name[0]))
        plt.plot(rate)
        plt.show()

    def __str__(self):
        return "cash: {}\nratio: {}".format(self.cash, self.ratio)
