from typing import List
from paho.mqtt.client import Client
from hub.mqtt_clients.base import MQTTClientBase


class PahoClient(MQTTClientBase):
    def __init__(self, host: str, port: int, keepalive: int):
        self._client = Client()
        self._host = host
        self._port = port
        self._keepalive = keepalive

        self._on_message, self._on_connect, self._subscription_topics = None, None, []

    def connect(self, subscription_topics: List[str], on_connect=None, on_message=None):
        self._client.on_connect = self.__connected
        self._client.on_message = self.__message_received

        self._on_message, self._on_connect, self._subscription_topics = on_message, on_connect, subscription_topics

        self._client.connect(self._host, self._port, self._keepalive)

    def __connected(self):
        for topic in self._subscription_topics:
            self._client.subscribe(topic)

        if self._on_connect:
            self._on_connect()

    def __message_received(self, client: Client, userdata, msg):
        if self._on_message:
            self._on_message(msg)

    def loop_background(self):
        self._client.loop_start()
