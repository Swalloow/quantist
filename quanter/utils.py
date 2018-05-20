from datetime import datetime


def convert_dt(year: int, month: int, day: int) -> str:
    return datetime(year, month, day).strftime('%Y-%m-%d %H:%M:%S')
