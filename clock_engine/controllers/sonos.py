from .base import BaseController
from soco import SoCo
from time import sleep


class SonosController(BaseController):

    def __init__(self, duration: int, ip_address: str) -> None:
        super().__init__()

        self.duration = duration

        # Initialize sonos speaker connection
        # todo: make this config data
        self.sonos = SoCo(ip_address)

    def _loop(self, cancellation_token) -> None:
        # todo: select station/track info to play
        self.sonos.volume = 0

        # Test parameters
        # todo: make this config data
        ending_volume = 40
        step_time = 1
        elapsed_time = 0

        # Start playing
        self.sonos.play()

        # Increment volume for duration of alarm
        while elapsed_time < self.duration and not cancellation_token():
            self.sonos.volume += max(min(int(elapsed_time / 100 * ending_volume), 100), 1)
            sleep(step_time)
            elapsed_time += step_time
