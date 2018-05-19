from datetime import datetime
from math import trunc


def convert_dt(year: int, month: int, day: int) -> str:
    return datetime(year, month, day).strftime('%Y-%m-%d %H:%M:%S')


def buy_price(cash: int, price: int) -> (int, int):
    return trunc(cash / price), trunc(cash / price) * price


def sell_price(count: int, price: int) -> int:
    return count * price
