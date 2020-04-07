from .base import BaseDriver
from .transitions.sonos import SonosWakeUpTransition
from hub.mqtt_clients.base import MQTTClientBase
from soco import SoCo
from paho.mqtt.client import Client


class SonosDriver(BaseDriver):
    def __init__(self, duration: int, ip_address: str, mqtt_client: MQTTClientBase):
        self.duration = duration

        # Initialize Sonos connection
        self.sonos = SoCo(ip_address)

        self.transitions = {
            'wake-up': SonosWakeUpTransition(self.duration, self.sonos)
        }

        super().__init__(['rise'], mqtt_client)

    def on_message(self, payload: str) -> None:
        if payload == 'alarm/30-min-warning':
            self.transitions['wake-up'].start()
