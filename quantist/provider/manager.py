import argparse
import os
from typing import List

import boto3
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


def save_all_stock():
    if not os.path.exists("{}/code.parquet".format(PATH)):
        save_code()

    df = pd.read_parquet("{}/code.parquet".format(PATH), engine='pyarrow')
    df = df[df.market == 'kospi']
    codes = df.code.tolist()
    loader = StockLoader('')
    for each in codes:
        print("-------------------------")
        print("{} start!!".format(each))
        loader.code = each
        items = loader.get_items('2017-08-01', '2018-05-18')
        print("first items : {}".format(items[0]))
        print("length : {}".format(len(items)))

        dynamodb = boto3.resource('dynamodb', 'ap-northeast-2')
        table = dynamodb.Table('stock')
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
        print("save finished!")


def find_code(corp: str) -> str:
    df = pd.read_parquet("{}/code.parquet".format(PATH), engine='pyarrow')
    return df[df.corp == corp].code


def get_price_by_entire(code: str, start_date: str, end_date: str) -> List[dict]:
    loader = StockLoader(code)
    return loader.get_items(start_date, end_date)


def get_kospi200_code() -> List[str]:
    raise NotImplementedError('TODO')


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
