"""
Test basic queue functionality

>>> from queues import queues
>>> import time
>>> queue_name = 'test_queues_%.f' % time.time()

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

Note that SQS doesn't guarantee that the message
we just wrote will be immediately available
>>> len(q)
1

Read from the queue
>>> q.read()
'test'

The queue should now be empty
Note that SQS doesn't guarantee an accurate count
>>> len(q)
0

>>> try:
...     queues.delete_queue(queue_name)
... except NotImplementedError:
...     print True
True
"""

if __name__ == "__main__":
    import doctest
    doctest.testmod()