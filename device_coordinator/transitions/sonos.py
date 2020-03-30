from .base import BaseTransition
from soco import SoCo
from time import sleep
from datetime import datetime


class SonosWakeUpTransition(BaseTransition):

    def __init__(self, duration: int, sonos: SoCo) -> None:
        super().__init__()

        self.duration = duration

        # Initialize sonos speaker connection
        # todo: make this config data
        self.sonos = sonos

    def _transition(self, cancellation_token: callable(bool)) -> None:
        print(datetime.now(), 'starting sonos loop')
        # todo: select station/track info to play
        self.sonos.volume = 0

        # Test parameters
        # todo: make this config data
        ending_volume = 5
        step_time = 1
        elapsed_time = 0

        # Start playing
        self.sonos.play()

        # Increment volume for duration of alarm
        while elapsed_time < self.duration and not cancellation_token():
            self.sonos.volume += max(min(int(elapsed_time / 100 * ending_volume), 100), 1)
            sleep(step_time)
            elapsed_time += step_time
