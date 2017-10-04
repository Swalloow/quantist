from config import Config
import requests


def send_message(channel, message):
    return requests.post(Config.SLACK_URI, json={
        "channel": channel,
        "text": message
    })
