import os


class Config:
    APP_NAME = 'rogers'
    DATABASE_URI = os.getenv("DATABASE_URI")
    SLACK_URI = os.getenv("SLACK_URI")


class Source:
    BITHUMB_URI = 'https://api.bithumb.com/public/ticker/'
    COINONE_URI = 'https://api.coinone.co.kr/ticker/'
    KORBIT_URI = 'https://api.korbit.co.kr/v1/ticker/detailed'
