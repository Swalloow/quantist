from multiprocessing import Manager
from multiprocessing import Pool

import pandas as pd
import requests
from bs4 import BeautifulSoup


class StockLoader(object):
    """Collect the index of each stock"""
    def __init__(self, code: str):
        self.url = "http://finance.naver.com/item/sise_day.nhn?code={}&page={}"
        self.code = code
        self.items = Manager().list()

    def get_last_page(self) -> int:
        response = requests.get(self.url.format(self.code, 1)).text
        bs = BeautifulSoup(response, "html.parser")
        page = bs.find('td', class_='pgRR')
        last_page = [a['href'] for a in page.find_all('a', href=True) if a.text][0][-3:]
        last_page = int(''.join(filter(str.isdigit, last_page)))
        return last_page + 1

    def parse(self, page: int):
        df = pd.read_html(self.url.format(self.code, page), header=0)[0]
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
        df['name'] = self.code
        df = df.dropna()
        df[['close', 'diff', 'open', 'high', 'low', 'volume']] \
            = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)

        self.items.append(df)

    def get_items(self):
        pool = Pool()
        last_page = self.get_last_page()
        if last_page > 21:
            last_page = 21

        pages = [i for i in range(1, last_page)]
        print("total pages: {}".format(len(pages)))
        pool.map(self.parse, pages)
        df = pd.concat(self.items)
        df = df[df['date'].between('2017-08-01', '2018-05-18', inclusive=True)]

        return df.to_dict(orient='records')
