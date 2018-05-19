from math import trunc
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
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

    @staticmethod
    def buy_price(cash: int, price: int) -> (int, int):
        return trunc(cash / price), trunc(cash / price) * price

    @staticmethod
    def sell_price(count: int, price: int) -> int:
        return count * price

    @staticmethod
    def plot_profit_change(buy: int, items: List[dict]):
        df = pd.DataFrame(items, columns=['name', 'date', 'close', 'diff'])
        rate = df.close.apply(lambda x: round((x - buy) / x * 100, 2)).tolist()
        plt.title("{} profit change".format(df.name[0]))
        plt.plot(rate)
        plt.show()

    def __str__(self):
        return "cash: {}\nratio: {}".format(self.cash, self.ratio)
