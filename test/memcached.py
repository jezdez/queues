"""
Test basic queue functionality

>>> from queues import queues
>>> import datetime
>>> queue_name = 'test_queues_%s' % datetime.datetime.now().isoformat()

Verify that the queue does not exist
>>> queue_name in queues.get_list()
False

Create the queue
>>> q = queues.Queue(queue_name)

Write to the queue
>>> q.write('test')
True

Verify that it is indeed in the list
>>> queue_name in queues.get_list()
True

Get the length of the queue
>>> len(q)
1

Read from the queue
>>> q.read()
'test'

The queue should now be empty
>>> len(q)
0

TODO: get rid of the queue?
"""

if __name__ == "__main__":
    import doctest
    doctest.testmod()