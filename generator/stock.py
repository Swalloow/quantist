from multiprocessing import Manager
from multiprocessing import Pool
from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup


class StockParser:
    def __init__(self, code: str):
        self.url = "http://finance.naver.com/item/sise_day.nhn?code={}&page={}"
        self.code = code
        self.items = Manager().list()

    def get_last_page(self) -> int:
        response = requests.get(self.url.format(self.code, 1)).text
        bs = BeautifulSoup(response, "html.parser")
        page = bs.find('td', class_='pgRR')
        last_page = [a['href'] for a in page.find_all('a', href=True) if a.text][0][-3:]
        return int(last_page) + 1

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
        df['date'] = df['date'].apply(lambda d: pd.to_datetime(d, format='%Y-%m-%d'))
        print(min(df['date']), max(df['date']), sep=', ')
        self.items.append(df)

    def get_items(self) -> List[pd.DataFrame]:
        pool = Pool()
        pages = [i for i in range(1, self.get_last_page())]
        pool.map(self.parse, pages)
        return self.items
