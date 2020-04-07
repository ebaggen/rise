from .base import BaseTransition
from phue import Bridge
from time import sleep
from datetime import datetime


class HueWakeUpTransition(BaseTransition):

    def __init__(self, duration: int, lights: Bridge.lights) -> None:
        super().__init__(duration)
        self.lights = lights

    def _transition(self, percent_complete: float, first_call: bool) -> None:

        if first_call:
            print(datetime.now(), 'starting hue loop')

        # Limit brightness between 1 and 254
        brightness = max(min(int(percent_complete * 100), 254), 1)
        for light in self.lights:
            light.on = True
            light.brightness = brightness
