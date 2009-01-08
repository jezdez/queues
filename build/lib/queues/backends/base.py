"Base queue class"

# Things to think about:
# - timeout/visibility timeout (boto)

class BaseQueue(object):
    """
    Abstract base class for queue backends.
    """
    
    def read(self):
        raise NotImplementedError

    def write(self, message):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

def create_queue():
    raise NotImplementedError

def delete_queue(name):
    raise NotImplementedError

def get_list():
    raise NotImplementedError