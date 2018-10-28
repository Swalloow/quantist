import os
import asyncio
import aiohttp
import redis
import pandas as pd
from bs4 import BeautifulSoup


PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/dataset"
URI = "http://finance.naver.com/item/sise_day.nhn?code={}&page={}"
r = redis.StrictRedis(host='localhost', port=6379, db=0)


async def get_last_page(bs):
    try:
        page = bs.find('td', class_='pgRR')
        last_page = [a['href'] for a in page.find_all('a', href=True) if a.text][0][-3:]
        last_page = int(''.join(filter(str.isdigit, last_page)))
    except AttributeError:
        return 2
    return last_page + 1


async def fetch_url(code, url):
    print('Starting {}'.format(url))
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            bs = BeautifulSoup(await resp.text(), 'html.parser')
            last_page = await get_last_page(bs)
            r.set(code, last_page)


if __name__ == '__main__':
    code_df = pd.read_parquet("{}/code.parquet".format(PATH), engine='pyarrow')
    code_df = code_df[code_df.market == 'kosdaq'][500:]
    codes = code_df.code.tolist()
    urls = [(each, URI.format(each, 1)) for each in codes]

    futures = [fetch_url(url, code) for url, code in urls]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(futures))
