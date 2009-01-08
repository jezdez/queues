import os
from queues import InvalidBackend

__all__ = ['backend']

# Handle QUEUE_BACKEND set from either DJANGO_SETTINGS_MODULE or an environment variable.
# If set both places, django takes precedence.
try:
    from django.conf import settings
    BACKEND = settings.get('QUEUE_BACKEND', None)
except:
    BACKEND = os.environ.get('QUEUE_BACKEND', None)

if not BACKEND:
    raise InvalidBackend("QUEUE_BACKEND not set.")

try:
    # Most of the time we'll be importing a bundled backend,
    # so look here first.  You might recall this pattern from
    # such web frameworks as Django.
    backend = __import__('queues.backends.%s' % BACKEND, {}, {}, [''])
except ImportError, e:
    # If that didn't work, try an external import.
    try:
        backend = __import__(BACKEND, {}, {}, [''])
    except ImportError:
        raise InvalidBackend("Unable to import QUEUE BACKEND '%s'" % BACKEND)
