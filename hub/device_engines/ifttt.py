from .base import BaseDriver
from requests import post
from datetime import datetime
from ..mqtt_clients.base import MQTTClientBase


class IFTTTDriver(BaseDriver):
    def __init__(self, mqtt_client: MQTTClientBase):
        super().__init__(['rise/alarm/wake-up'], mqtt_client)

    def on_message(self, payload: str) -> None:
        post('https://maker.ifttt.com/trigger/rise_alarm_wake_up/with/key/bAq-eAumbJA9TH6s-gG_JE')
