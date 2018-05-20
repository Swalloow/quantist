from urllib import parse

import pandas as pd

MARKET_CODE_DICT = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt',
    'konex': 'konexMkt'
}


class CodeLoader(object):
    """Collect the code of each stock"""
    def __init__(self):
        self.url = "kind.krx.co.kr/corpgeneral/corpList.do"

    def get_items(self, market: str=None):
        params = {'method': 'download', 'searchType': 13}

        if market.lower() in MARKET_CODE_DICT:
            params['marketType'] = MARKET_CODE_DICT[market]

        params = parse.urlencode(params)
        request_url = parse.urlunsplit(['http', self.url, '', params, ''])

        df = pd.read_html(request_url, header=0)[0]
        df = df.rename(columns={
            '회사명': 'corp',
            '종목코드': 'code',
            '업종': 'industry',
            '주요제품': 'product',
            '상장일': 'opening_date',
            '결산월': 'closing_month',
            '대표자명': 'ceo',
            '홈페이지': 'homepage',
            '지역': 'local'
        })
        df['market'] = market
        df.code = df.code.map('{:06d}'.format)
        return df
