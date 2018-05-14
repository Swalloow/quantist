import argparse
import os

import pandas as pd

from stock import StockLoader


def save_items(code: str):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    loader = StockLoader(code)
    df = loader.get_items()
    df.to_parquet("{}/dataset/{}.parquet".format(path, code), engine='pyarrow')


def load_items(code: str) -> pd.DataFrame:
    loader = StockLoader(code)
    return loader.get_items()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--code', required=True)
    args = parser.parse_args()
    save_items(args.code)
