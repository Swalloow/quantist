import os
import time
import asyncio
import redis
import pandas as pd
from bs4 import BeautifulSoup
from multiprocessing import Pool


PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/dataset"
URI = "http://finance.naver.com/item/sise_day.nhn?code={}&page={}"
r = redis.StrictRedis(host='localhost', port=6379, db=0)


def parse_html(code):
    print('Start {}'.format(code))
    dfs = []
    for page in get_last_page(code):
        df = pd.read_html(URI.format(code, page), header=0)[0]
        df = df.rename(columns={
            '날짜': 'date',
            '종가': 'close',
            '전일비': 'diff',
            '시가': 'open',
            '고가': 'high',
            '저가': 'low',
            '거래량': 'volume'
        })
        df['date'] = df['date'].apply(lambda d: str(pd.to_datetime(d)))
        df['name'] = str(code)
        df = df.dropna()
        df[['close', 'diff', 'open', 'high', 'low', 'volume']] \
            = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
        dfs.append(df)
    result = pd.concat(dfs)
    result.to_parquet("{}/{}.parquet".format(PATH, code), engine='pyarrow')


def get_last_page(code):
    last_page = int(r.get(code))
    return range(1, 30 if last_page > 30 else last_page)


if __name__ == '__main__':
    start_time = time.time()
    code_df = pd.read_parquet("{}/code.parquet".format(PATH), engine='pyarrow')
    code_df = code_df[code_df.market == 'kosdaq']
    codes = code_df.code.tolist()

    # Version1 (67.91s)
    # for each in codes:
    #     print('Starting {}'.format(each))
    #     for page in get_last_page(each):
    #         parse_html(each, URI.format(each, page))

    # Version2 (87.50s)
    # for each in codes:
    #     urls = [(each, URI.format(each, page)) for page in get_last_page(each)]
    #     futures = [parse_html(code, url) for code, url in urls]
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(asyncio.wait(futures))

    # Version3 (26.38s)
    pool = Pool(processes=4)
    pool.map(parse_html, codes)
    print("--- %s seconds ---" % (time.time() - start_time))
