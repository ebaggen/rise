from .base import BaseTransition
from soco import SoCo
from datetime import datetime


class SonosWakeUpTransition(BaseTransition):

    def __init__(self, duration: int, sonos: SoCo) -> None:
        super().__init__(duration)
        self.sonos = sonos

    def _transition(self, percent_complete: float, first_call: bool) -> None:

        if first_call:
            # todo: select station/track info to play

            # Set volume to 0
            self.sonos.volume = 0

            # Start playing currently selected media
            self.sonos.play()

            # Test parameters

        self.sonos.volume = percent_complete * 7
