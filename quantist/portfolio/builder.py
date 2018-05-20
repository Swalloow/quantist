from math import trunc

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_style('darkgrid')


class Portfolio(object):
    def __init__(self, cash: int, ratio: dict=None):
        self.cash = cash
        self.ratio = {} if ratio is None else ratio

    def __str__(self):
        return "cash: {}\nratio: {}".format(self.cash, self.ratio)

    def update(self, stock: list, weight: list):
        self.ratio = dict(zip(stock, weight))

    def calculate_profit(self, cash: int, buy: int, sell: int) -> int:
        cnt, buy = self.buy_price(cash, buy)
        sell = self.sell_price(cnt, sell)
        return sell - buy

    @staticmethod
    def calculate_mean_var(mean, var, weight):
        port_ret = np.dot(weight, mean)
        port_std = np.dot(np.dot(weight, var), weight.T)
        return port_ret, port_std

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
    def plot_profit_change(df: pd.DataFrame):
        stock = df.columns.tolist()
        for each in stock:
            plt.title("profit change")
            plt.plot(df[each].tolist())
        plt.legend(stock, loc='upper left')
        plt.show()
