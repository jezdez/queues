"""
Backend for beanstalkd queue.

This backend requires the beanstalkc library to be installed.
"""

from queues.backends.base import BaseQueue
from queues import InvalidBackend, QueueException
import os


try:
    import beanstalkc
except ImportError:
    raise InvalidBackend("Unable to import the beanstalkc library.")

try:
    from django.conf import settings
    CONN = getattr(settings, 'QUEUE_BEANSTALKD_CONNECTION', None)
except:
    CONN = os.environ.get('QUEUE_BEANSTALKD_CONNECTION', None)

if not CONN:
    raise InvalidBackend("QUEUE_BEANSTALKD_CONNECTION not set.")


class Queue(BaseQueue):
    def __init__(self, name='default'):
        host, port = CONN.split(':')
        self._connection = beanstalkc.Connection(host=host, port=int(port))
        self.backend = 'beanstalkd'
        self.name = name
        self._connection.use(name)

    def read(self):
        try:
            job = self._connection.reserve()
            message = job.body
            job.delete()
            return message
        except (beanstalkc.DeadlineSoon, beanstalkc.CommandFailed, beanstalkc.UnexpectedResponse), e:
            raise QueueException, e

    def write(self, message):
        try:
            return self._connection.put(message)
        except (beanstalkc.CommandFailed, beanstalkc.UnexpectedResponse), e:
            raise QueueException, e

    def __len__(self):
        try:
            return int(self._connection.stats().get('current-jobs-ready', 0))
        except (beanstalkc.CommandFailed, beanstalkc.UnexpectedResponse), e:
            raise QueueException, e

    def __repr__(self):
        return "<Queue %s>" % self.name

def create_queue():
    """This isn't required, so we noop.  Kept here for swapability."""
    return True

def delete_queue(name):
    """Beanstalkd backends don't provide a way to do this."""
    raise NotImplementedError

def get_list():
    """Beanstalkd backends don't provide a way to do this."""
    raise NotImplementedError
