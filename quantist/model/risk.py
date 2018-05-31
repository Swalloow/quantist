import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as sco

from provider.handler import DynamoDBHandler
from utils import convert_dt


class MarkowitzModel(object):
    def __init__(self, stock):
        self.stock = stock
        self.ratio = []

    def load_data(self) -> pd.DataFrame:
        start_date = convert_dt(2017, 9, 1)
        end_date = convert_dt(2018, 5, 20)
        db = DynamoDBHandler('stock')
        dfs = []
        for each in self.stock:
            items = db.get_price_by_date(each, start_date, end_date)
            df = pd.DataFrame(items, columns=['name', 'date', 'close'])
            df['close'] = df.close.astype(int)
            df = df.set_index('date').sort_index()
            df = df.drop(['name'], axis=1).rename(index=str, columns={"close": str(each)})
            dfs.append(df)

        df = pd.concat(dfs, axis=1)
        return df

    def optimize(self, opt='max'):
        def statistics(weights):
            weights = np.array(weights)
            pret = np.sum(rets.mean() * weights) * 252
            pvol = np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights)))
            return np.array([pret, pvol, pret / pvol])

        def min_func_sharpe(weights):
            return -statistics(weights)[2]

        def min_func_variance(weights):
            return statistics(weights)[1] ** 2

        df = self.load_data()
        noa = len(self.stock)
        np.random.seed(2)
        weights = np.random.random(noa)
        weights /= np.sum(weights)
        rets = np.log(df / df.shift(1))

        prets = []
        pvols = []
        for p in range(2500):
            weights = np.random.random(noa)
            weights /= np.sum(weights)
            prets.append(np.sum(rets.mean() * weights) * 252)
            pvols.append(np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights))))
        prets = np.array(prets)
        pvols = np.array(pvols)

        cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bnds = tuple((0, 1) for _ in range(noa))
        opts = sco.minimize(min_func_sharpe if opt == 'max' else min_func_variance,
                            noa * [1. / noa, ], method='SLSQP',
                            bounds=bnds, constraints=cons)
        plt.scatter(pvols, prets, c=prets / pvols, marker='o')
        plt.grid(True)
        plt.xlabel('expected volatility')
        plt.ylabel('expected return')
        plt.colorbar(label='Sharpe ratio')

        pt_opts = statistics(opts['x']).round(3)
        plt.scatter(pt_opts[1], pt_opts[0], marker="v", s=100, alpha=0.3, color='red')
        plt.show()
        return list(pt_opts)

    def plot_sharpe_ratio(self):
        raise NotImplementedError('TODO')
