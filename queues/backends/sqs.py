"""
Backend for Amazon's Simple Queue Service.

This backend requires that the boto library is installed.
"""

from queues.backends.base import BaseQueue
from queues import InvalidBackend, QueueException
import os

try:
    from boto.sqs.connection import SQSConnection
    from boto.sqs.message import Message
    from boto.exception import SQSError
except ImportError:
    raise InvalidBackend("Unable to import boto.")

try:
    from django.conf import settings
    KEY = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    SECRET = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
except:
    KEY = os.environ.get('AWS_ACCESS_KEY_ID', None)
    SECRET = os.environ.get('AWS_SECRET_ACCESS_KEY', None)

if not KEY:
    raise InvalidBackend("AWS_ACCESS_KEY_ID not set.")
if not SECRET:
    raise InvalidBackend("AWS_SECRET_ACCESS_KEY not set.")

# ... and one connection to bind them.
connection = SQSConnection()

class Queue(BaseQueue):
    def __init__(self, name):
        self.name = name
        self.backend = 'sqs'
        self._connection = connection
        self._queue = self._connection.get_queue(self.name)
        if not self._queue:
            self._queue = self._connection.create_queue(name)

    def read(self):
        try:
            m = self._queue.read()
            if not m:
                return None
            else:
                self._queue.delete()
                return m.get_body()
        except SQSError, e:
            raise QueueException, "%s" % e.code

    def write(self, message):
        try:
            m = Message()
            m.set_body(message)
            return self._queue.write(m)
        except SQSError, e:
            raise QueueException, "%s" % e.code

    def __len__(self):
        try:
            length = self._queue.count()
            if not length:
                length = 0
            return int(length)
        except SQSError, e:
            raise QueueException, "%s" % e.code

    def __repr__(self):
        return "<Queue %s>" % self.name

def create_queue(name):
    """Create a queue for the given name."""
    try:
        return connection.create_queue(name)
    except SQSError, e:
        raise QueueException, "%s" % e.code

def delete_queue(name):
    """
    Deletes a queue and any messages in it.
    """
    # TODO: too fragile.
    try:
        return connection.get_status('DeleteQueue', None, '/' + name)
    except SQSError, e:
        raise QueueException, "%s" % e.code

def get_list():
    """
    Get a list of names for all queues.  Returns a list of ``queues.backends.sqs.Queue`` objects.
    """
    # TODO: too fragile.
    try:
        return [q.id[1:] for q in connection.get_all_queues()]
    except SQSError, e:
        raise QueueException, "%s" % e.code
