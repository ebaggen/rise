from enum import Enum
from threading import Thread
from time import sleep
from queue import SimpleQueue


class BaseController:
    class Actions(Enum):
        Start = 1
        Stop = 2
        Terminate = 3

    class Status(Enum):
        Idle = 1
        Running = 2
        Terminated = 3

    def __init__(self, callback):
        self.event_queue = SimpleQueue()

        self.status = self.Status.Idle

        self.callback = callback

        self.event_thread = Thread(target=self.__daemon)
        self.event_thread.setDaemon(True)
        self.event_thread.start()

    def start(self):
        if self.status == self.status.Terminated:
            raise Exception('Controller is terminated.')
        else:
            self.event_queue.put_nowait(self.Actions.Start)

    def stop(self):
        if self.status == self.status.Terminated:
            raise Exception('Controller is terminated.')
        else:
            self.event_queue.put_nowait(self.Actions.Stop)

    def terminate(self):
        self.event_queue.put_nowait(self.Actions.Terminate)
        self.event_thread.join()

    def __daemon(self):

        while self.status != self.Status.Terminated:

            if not self.event_queue.empty():
                command = self.event_queue.get()
                if command == self.Actions.Start:
                    self.status = self.Status.Running
                elif command == self.Actions.Stop:
                    self.status = self.Status.Idle
                elif command == self.Actions.Abort:
                    self.status = self.Status.Aborted
                else:
                    # todo: raise an error that a bad command was received
                    pass

            if self.status == self.Status.Running:
                self.callback()

            sleep(1)
