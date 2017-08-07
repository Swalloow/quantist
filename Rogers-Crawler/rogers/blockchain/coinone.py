from datetime import datetime

from config import Source
from ..model.models import Coinone
import requests


class ParserCoinone:
    def __init__(self):
        self.model = Coinone
        self.url = Source.COINONE_URI
        self.currency = ["btc", "eth"]

    def get_response(self, params):
        try:
            response = requests.get(self.url, params)
            return response

        except requests.exceptions.ConnectionError:
            # TODO: Slack notification
            return "Connection Failed!"

    def parse(self, response, currency):
        result = response.json()
        price = result["last"]
        volume = result["volume"]
        self.model = Coinone(datetime.utcnow(), price, volume, currency)
        return self.model
