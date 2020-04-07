from typing import List
from abc import ABC, abstractmethod
from ..mqtt_clients import MQTTClientBase


class BaseDriver(ABC):
    def __init__(self, subscription_topics: List[str], mqtt_client: MQTTClientBase):
        self.mqtt_client = mqtt_client
        self.subscription_topics = subscription_topics

        self.mqtt_client.connect(subscription_topics, self.on_connect, self.on_message)

        self.mqtt_client.loop_background()

    @abstractmethod
    def on_message(self, payload: str) -> None:
        return

    def on_connect(self) -> None:
        return
