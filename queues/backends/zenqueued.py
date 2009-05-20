"""
Backend for zenqueue queue.

This backend requires the zenqueue library to be installed. It uses the
HTTP connection to a zenqueue server and the async bits.
"""

from queues.backends.base import BaseQueue
from queues import InvalidBackend, QueueException
import os


try:
    from zenqueue.client import QueueClient
    # from zenqueue.queue.Queue import Timeout
except ImportError:
    raise InvalidBackend("Unable to import the zenqueue library.")

try:
    from django.conf import settings
    CONN = getattr(settings, 'QUEUE_ZENQUEUE_CONNECTION', None)
    METHOD = getattr(settings, 'QUEUE_ZENQUEUE_METHOD', 'http')
except:
    CONN = os.environ.get('QUEUE_ZENQUEUE_CONNECTION', None)
    METHOD = os.environ.get('QUEUE_ZENQUEUE_METHOD', 'http')

if not CONN:
    raise InvalidBackend("QUEUE_ZENQUEUE_CONNECTION not set.")

try:
    host, port = CONN.split(':')
except ValueError:
    raise InvalidBackend("QUEUE_ZENQUEUE_CONNECTION should be in the format host:port (such as localhost:3000).")

class Queue(BaseQueue):
    def __init__(self, name='default'):
        self._connection = QueueClient(method=METHOD, host=host, port=int(port), mode='async')
        self.backend = 'zenqueued'
        self.name = name

    def read(self):
        try:
            message = self._connection.pull()
            return message
        except Exception, e:
            raise QueueException, e

    def write(self, message):
        try:
            self._connection.push(message)
            # push only exposes operation success/fail as a DEBUG logging message
            return True
        except Exception, e:
            raise QueueException, e

    def __len__(self):
        """zenqueue backends don't provide a way to do this."""
        raise NotImplementedError

    def __repr__(self):
        return "<Queue %s>" % self.name

def create_queue():
    """This isn't required, so we noop.  Kept here for swapability."""
    return True

def delete_queue(name):
    """zenqueue backends don't provide a way to do this."""
    raise NotImplementedError

def get_list():
    """zenqueue backends don't provide a way to do this."""
    raise NotImplementedError
