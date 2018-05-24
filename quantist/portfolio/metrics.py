from typing import List

import numpy as np
import pandas as pd


def daily_mean(df: pd.DataFrame, weight: List[float]):
    w = np.array(weight).T
    return np.dot(w, df.mean())


def variance(df: pd.DataFrame, weight: List[float], corr: bool=False):
    w = np.array(weight).T
    var = df.cov() if corr is False else df.corr()
    return np.dot(np.dot(w, var), w.T)


def sharpe_ratio():
    raise NotImplementedError('TODO')


def mdd():
    raise NotImplementedError('TODO')
