from .base import BaseDriver
from ..mqtt_clients.base import MQTTClientBase
from .transitions.hue import HueWakeUpTransition
from phue import Bridge


class HueDriver(BaseDriver):
    def __init__(self, duration: int, ip_address: str, mqtt_client: MQTTClientBase) -> None:

        # Initialize Hue connection
        self.bridge = Bridge(ip_address)

        self.transitions = {
            'wake-up': HueWakeUpTransition(duration, self.bridge.lights)
        }

        super().__init__(['rise'], mqtt_client)

    def on_message(self, payload: str) -> None:
        if payload == 'alarm/30-min-warning':
            self.transitions['wake-up'].start()
