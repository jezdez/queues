"""
A pluggable abstract queueing API designed to be used within a Django project
but useful within a general Python application too.  The design is modeled
after a pluggable backend system ala django.core.cache.

Backends that merit investigation

x http://aws.amazon.com/ (SQS)
* http://code.google.com/p/django-queue-service/
x https://rubyforge.org/projects/starling/ (memcache)
x http://code.google.com/p/sparrow/ (memcache)
* http://xph.us/software/beanstalkd/ (not persistent)
* http://code.google.com/p/peafowl/ (python/memcache)
* http://memcachedb.org/memcacheq/ (memcache)

Other backends that might be worth checking out

* http://stompserver.rubyforge.org/
* http://www.spread.org/
* http://code.google.com/p/stomperl/
* RabbitMQ
"""
import os

__version__ = "0.3"

class InvalidBackend(Exception):
    pass

class QueueException(Exception):
    pass

# TODO: raise exceptions when stuff doesn't get stored/returned properly?
# i.e. unified API and handle what each backend returns.

# Handle QUEUE_BACKEND set from either DJANGO_SETTINGS_MODULE or an environment variable.
# If set both places, django takes precedence.
try:
    from django.conf import settings
    BACKEND = getattr(settings, 'QUEUE_BACKEND', None)
except:
    BACKEND = os.environ.get('QUEUE_BACKEND')

if not BACKEND:
    raise InvalidBackend("QUEUE_BACKEND not set.")

# Set up queues.queues to point to the proper backend.
try:
    # Most of the time we'll be importing a bundled backend,
    # so look here first.  You might recall this pattern from
    # such web frameworks as Django.
    queues = __import__('queues.backends.%s' % BACKEND, {}, {}, [''])
except ImportError, e:
    # If that didn't work, try an external import.
    try:
        queues = __import__(BACKEND, {}, {}, [''])
    except ImportError:
        raise InvalidBackend("Unable to import QUEUE BACKEND '%s'" % BACKEND)