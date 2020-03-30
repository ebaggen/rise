from .base import BaseDriver
from requests import post
from paho.mqtt.client import Client
from datetime import datetime


class IFTTTDriver(BaseDriver):
    def __init__(self) -> None:
        super().__init__(['rise/alarm/wake-up'])

    def on_message(self, client: Client, userdata, msg) -> None:
        print(datetime.now(), 'calling phone')
        post('https://maker.ifttt.com/trigger/rise_alarm_wake_up/with/key/bAq-eAumbJA9TH6s-gG_JE')
