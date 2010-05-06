"""
Backend for redis.

Requires redis.py from the redis source (found in client-libraries/python).
"""

from queues.backends.base import BaseQueue
from queues import InvalidBackend, QueueException
import os

try:
    import redis
except ImportError:
    raise InvalidBackend("Unable to import redis.")

CONN = DB = None

try:
    from django.conf import settings
    CONN = getattr(settings, 'QUEUE_REDIS_CONNECTION', None)
    DB = getattr(settings, 'QUEUE_REDIS_DB', None)
except:
    CONN = os.environ.get('QUEUE_REDIS_CONNECTION', None)
    DB = os.environ.get('QUEUE_REDIS_DB', None)

if not CONN:
    raise InvalidBackend("QUEUE_REDIS_CONNECTION not set.")

try:
    host, port = CONN.split(':')
except ValueError:
    raise InvalidBackend("QUEUE_REDIS_CONNECTION should be in the format host:port (such as localhost:6379).")

try:
    port = int(port)
except ValueError:
    raise InvalidBackend("Port portion of QUEUE_REDIS_CONNECTION should be an integer.")

def _get_connection(host=host, port=port, db=DB):
    kwargs = {'host' : host, 'port' : port}
    if DB:
        kwargs['db'] = DB
    return redis.Redis(**kwargs)

class Queue(BaseQueue):
    def __init__(self, name):
        try:            
            self.name = name
            self.backend = 'redis'
            kwargs = {'host' : host, 'port' : int(port)}
            if DB:
                kwargs['db'] = DB
            self._connection = _get_connection()
        except redis.RedisError, e:
            raise QueueException, "%s" % e

    def read(self):
        try:
            return self._connection.lpop(self.name)
        except redis.RedisError, e:
            raise QueueException, "%s" % e

    def write(self, value):
        try:
            resp = self._connection.lpush(self.name, value)
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
    """Delete a queue"""
    try:
        resp = _get_connection().delete(name)
        if resp and resp == 1:
            return True
        else:
            return False
    except redis.RedisError, e:
        raise QueueException, "%s" % e

def get_list():
    return _get_connection().keys('*')
