from typing import List
from Adafruit_IO import MQTTClient
from hub.mqtt_clients.base import MQTTClientBase


class AdafruitIOClient(MQTTClientBase):
    def __init__(self, username: str, key: str):
        self._client = MQTTClient(username, key)

        self._on_message, self._on_connect, self._subscription_topics = None, None, []

    def connect(self, subscription_topics: List[str], on_connect=None, on_message=None):
        self._client.on_connect = self.__connected
        self._client.on_message = self.__message_received

        self._on_message, self._on_connect, self._subscription_topics = on_message, on_connect, subscription_topics

        self._client.connect()

    def __connected(self, client):
        for topic in self._subscription_topics:
            client.subscribe(topic)
        if self._on_connect:
            self._on_connect()

    def __message_received(self, client, feed_id, payload):
        print('adafruit io: ', payload)
        if self._on_message:
            self._on_message(payload)

    def loop_background(self):
        self._client.loop_background()
