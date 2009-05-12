"""
Backend for redis.

Requires redis.py from the redis source (found in client-libraries/python).
"""

from queues.backends.base import BaseQueue
from queues import InvalidBackend, QueueException

try:
    import redis
except ImportError:
    raise InvalidBackend("Unable to import redis.")

# TODO: Import host, port, db

class Queue(BaseQueue):
    def __init__(self, name):
        try:            
            self.name = name
            self.backend = 'redis'
            self._connection = redis.Redis()
        except redis.RedisError, e:
            raise QueueException, "%s" % e

    def read(self):
        try:
            return self._connection.pop(self.name)
        except redis.RedisError, e:
            raise QueueException, "%s" % e

    def write(self, value):
        try:
            resp = self._connection.push(self.name, value)
            if resp == 'OK':
                return True
            else:
                return False
        except redis.RedisError, e:
            raise QueueException, "%s" % e

    def __len__(self):
        try:
            return self._connection.llen(self.name)
        except redis.RedisError, e:
            raise QueueException, "%s" % e

    def __repr__(self):
        return "<Queue %s>" % self.name

def create_queue():
    """This isn't required, so we noop.  Kept here for swapability."""
    return True

def delete_queue(name):
    try:
        resp = redis.Redis().delete(name)
        if resp:
            return True
        else:
            return False
    except redis.RedisError, e:
        raise QueueException, "%s" % e

def get_list():
    return redis.Redis().keys('*')
