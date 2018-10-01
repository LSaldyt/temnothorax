from functools import wraps

from ant import Ant

def transition(**kwargs):
    for key in kwargs:
        assert key in Ant._fields, 'Invalid transition key: {}'.format(key)
    def modifier(ant):
        return ant._replace(**kwargs)
    return modifier
