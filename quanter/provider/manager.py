import argparse
import os

import pandas as pd

from code import CodeLoader
from stock import StockLoader

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/dataset"


def save_code():
    market = "kospi kosdaq".split()
    loader = CodeLoader()
    for each in market:
        df = loader.get_items(each)
        print(each, len(df), sep=', ')
    dfs = [loader.get_items(each) for each in market]
    df = pd.concat(dfs)
    df.to_parquet("{}/code.parquet".format(PATH), engine='pyarrow')


def save_single_stock(code: str):
    loader = StockLoader(code)
    items = loader.get_items()
    print("first items : {}".format(items[0]))
    print("length : {}".format(len(items)))


def save_all_stock():
    if not os.path.exists("{}/code.parquet".format(PATH)):
        save_code()

    df = pd.read_parquet("{}/code.parquet".format(PATH), engine='pyarrow')
    for each in df.code.tolist():
        print("-------------------------")
        print("{} start!!".format(each))
        save_single_stock(each)


def find_code(corp: str) -> str:
    df = pd.read_parquet("{}/code.parquet".format(PATH), engine='pyarrow')
    return df[df.corp == corp].code.values[0]


def load_items(code: str) -> pd.DataFrame:
    return pd.read_parquet("{}/{}.parquet".format(PATH, code), engine='pyarrow')


if __name__ == '__main__':
    import time

    parser = argparse.ArgumentParser()
    # parser.add_argument('command', choices=sorted(manager.commands))
    parser.add_argument('--code')
    args = parser.parse_args()

    start_time = time.time()
    # save_code()
    save_all_stock()
    print("--- %s seconds ---" % (time.time() - start_time))
