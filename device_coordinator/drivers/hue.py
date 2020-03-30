from .base import BaseDriver
from ..transitions.hue import HueWakeUpTransition
from phue import Bridge
from paho.mqtt.client import Client


class HueDriver(BaseDriver):
    def __init__(self, duration: int, ip_address: str) -> None:
        self.duration = duration

        # Initialize Hue connection
        self.bridge = Bridge(ip_address)
        self.lights = self.bridge.lights

        self.transitions = {
            'wake-up': HueWakeUpTransition(self.duration, self.lights)
        }

        super().__init__(['rise/alarm/30-min-warning'])

    def on_message(self, client: Client, userdata, msg) -> None:
        self.transitions['wake-up'].start()
