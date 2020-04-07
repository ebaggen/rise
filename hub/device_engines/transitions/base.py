from threading import Thread
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from time import sleep

'''
BaseTransition implements the base threading functionality for Rise transitions, like Hue and Sonos.
Child classes must call BaseTransition's constructor and override the _loop() method.

start() and stop() is handled by the BaseController.

Starting the action spins off a new thread. Only one thread is allowed per device_engines. If a device_engines is attempting
to start an already active process, an exception will be thrown. Higher level code should check is_active() before
trying to use a device_engines.

Stopping the action is done through a cancellation token. Simply raising the token will end the thread. The cancellation
token must be implemented by the child class!
'''


class BaseTransition(ABC):

    def __init__(self, duration: int) -> None:
        self.thread = Thread()
        self.cancellation_token = False
        self.duration = duration

    def start(self) -> None:
        if not self.is_active():
            self.thread = Thread(target=self.__loop, args=(lambda: self.cancellation_token,))
            self.thread.start()
        else:
            raise Exception('Thread already exists.')

    def stop(self) -> None:
        if self.is_active():
            self.cancellation_token = True
            self.thread.join()
            self.cancellation_token = False

    def is_active(self) -> bool:
        return self.thread.is_alive()

    # The concrete class must implement this method as the logic for each step in the transition loop
    @abstractmethod
    def _transition(self, percent_complete: float, first_call: bool) -> None:
        return

    def __loop(self, cancellation_token) -> None:
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=self.duration)

        current_time = start_time
        first_call = True

        while current_time < end_time and not cancellation_token():
            # Percent complete = elapsed time since start divided by the total duration
            percent_complete = (current_time.timestamp() - start_time.timestamp()) / self.duration
            self._transition(percent_complete, first_call)

            sleep(1)

            # Update current time
            current_time = datetime.now()

            # Set first call false. It should only be true on the first loop iteration
            if first_call:
                first_call = False
