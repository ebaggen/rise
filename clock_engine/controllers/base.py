from threading import Thread

'''
BaseController implements the base threading functionality for Rise controllers, like Hue and Sonos.
Child classes must call BaseController's constructor and override the _loop() method.

start() and stop() is handled by the BaseController.

Starting the action spins off a new thread. Only one thread is allowed per controller. If a controller is attempting
to start an already active process, an exception will be thrown. Higher level code should check is_active() before
trying to use a controller.

Stopping the action is done through a cancellation token. Simply raising the token will end the thread. The cancellation
token must be implemented by the child class!
'''


class BaseController:

    def __init__(self) -> None:
        self.thread = Thread()
        self.cancellation_token = False

    def start(self) -> None:
        if not self.is_active():
            self.thread = Thread(target=self._loop, args=(lambda: self.cancellation_token,))
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

    def _loop(self, cancellation_token) -> None:
        raise NotImplementedError
