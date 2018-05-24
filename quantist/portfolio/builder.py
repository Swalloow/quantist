from datetime import datetime
from math import trunc
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from metrics import (
    daily_mean,
    variance,
    winning_ratio
)

sns.set_style('darkgrid')


class Portfolio(object):
    def __init__(self, cash: int, ratio: dict=None):
        self.cash = cash
        self.stock = []
        self.weight = []
        self.ratio = {} if ratio is None else ratio

    def __str__(self):
        return "cash: {}\nratio: {}".format(self.cash, self.ratio)

    def update(self, stock: list, weight: list):
        self.stock = stock
        self.weight = weight
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
    def profit_ratio(buy: int, sell: int) -> float:
        return round((sell - buy) / sell * 100, 2)

    def report(self, df: pd.DataFrame, records: List[set]):
        mean = daily_mean(df, self.weight)
        var = variance(df, self.weight, corr=True)

        col = ['stock', 'ratio', 'seed', 'profit', 'holding', 'profit_rate']
        report = pd.DataFrame.from_records(records, columns=col)
        total_profit = sum(report.profit.tolist())
        total_profit_rate = round((total_profit / self.cash) * 100, 2)
        winning = winning_ratio(report.profit.tolist())

        print("-----------------------------------------------")
        print("total profit: {} / {}%".format(total_profit, total_profit_rate))
        print("portfolio mean: {}".format(mean))
        print("portfolio variance: {}".format(var))
        print("portfolio winning ratio: {}%".format(winning))
        print("-----------------------------------------------")
        print(report)
        self.plot_profit_change(df)

    @staticmethod
    def plot_profit_change(df: pd.DataFrame):
        stock = df.columns.tolist()
        date = [datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in df.index.tolist()]
        for each in stock:
            plt.title("profit change")
            plt.plot(date, df[each].tolist())
            plt.gcf().autofmt_xdate()
        plt.legend(stock, loc='upper left')
        plt.show()
