from .base import BaseDriver
from ..transitions.sonos import SonosWakeUpTransition
from soco import SoCo
from paho.mqtt.client import Client


class SonosDriver(BaseDriver):
    def __init__(self, duration: int, ip_address: str) -> None:
        self.duration = duration

        # Initialize Sonos connection
        self.sonos = SoCo(ip_address)

        self.transitions = {
            'wake-up': SonosWakeUpTransition(self.duration, self.sonos)
        }

        super().__init__(['rise/alarm/30-min-warning'])

    def on_message(self, client: Client, userdata, msg) -> None:
        self.transitions['wake-up'].start()
