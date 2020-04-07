from abc import ABC, abstractmethod
from typing import List


class MQTTClientBase(ABC):

    @abstractmethod
    def connect(self, subscription_topics: List[str], on_connect=None, on_message=None):
        return

    @abstractmethod
    def loop_background(self):
        return
