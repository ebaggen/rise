from .base import BaseTransition
from phue import Bridge
from time import sleep
from datetime import datetime


class HueWakeUpTransition(BaseTransition):

    def __init__(self, duration: int, lights: Bridge.lights) -> None:
        super().__init__()

        self.duration = duration
        self.lights = lights

    def _loop(self, cancellation_token) -> None:
        print(datetime.now(), 'starting hue loop')
        # Test parameters
        # todo: make this config data
        ending_brightness = 100
        step_time = 1
        elapsed_time = 0

        while elapsed_time < self.duration and not cancellation_token():
            percent_complete = elapsed_time / self.duration * 100
            brightness_percent = percent_complete / 100 * ending_brightness
            brightness = max(min(int(brightness_percent / 100 * 254), 254), 1)
            for light in self.lights:
                light.on = True
                light.brightness = brightness

                # todo: implement color changing functionality

            sleep(step_time)
            elapsed_time += step_time
