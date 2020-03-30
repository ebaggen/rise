from typing import List

from paho.mqtt.client import Client


class BaseDriver:
    def __init__(self, subscription_topics: List[str], host: str = 'localhost', port: int = 1883, keepalive: int = 60):
        self.client = Client()
        self.subscription_topics = subscription_topics
        self.client.connect(host, port, keepalive)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_start()

    def on_message(self, client: Client, userdata, msg) -> None:
        pass

    def on_connect(self, client: Client, userdata, flags, rc) -> None:
        print('Connected with result code ' + str(rc))
        for topic in self.subscription_topics:
            self.client.subscribe(topic)
