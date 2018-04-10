import argparse

import pandas as pd

from stock import StockParser

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--code', required=True)
    args = parser.parse_args()

    parser = StockParser(args.code)
    items = parser.get_items()
    df = pd.concat(items)
    df.to_pickle("../dataset/{}.p".format(args.code))
