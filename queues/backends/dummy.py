"""
A dummy queue that uses Python's built-in Queue class.

Useful for testing but likely not much else.
"""
import Queue as queue
from queues import QueueException
from queues.backends.base import BaseQueue


dummy_queue = queue.Queue()


class Queue(BaseQueue):
    def __init__(self, name='default'):
        self.queue = dummy_queue
        self.backend = 'dummy'
        self.name = name

    def read(self):
        try:
            message = self.queue.get(block=False)
            self.queue.task_done()
            return message
        except queue.Empty, e:
            raise QueueException("The queue is empty.")

    def write(self, message):
        try:
            return self.queue.put(message)
        except queue.Full, e:
            raise QueueException("The queue is full.")

    def __len__(self):
        return self.queue.qsize()

    def __repr__(self):
        return "<Queue %s>" % self.name


def create_queue():
    """This isn't required, so we noop.  Kept here for swapability."""
    return True


def delete_queue(name):
    """Just start afresh."""
    try:
        while True:
            dummy_queue.get(block=False)
    except queue.Empty:
        # Yay, exhausted.
        pass


def get_list():
    """No way to do this."""
    raise NotImplementedError
