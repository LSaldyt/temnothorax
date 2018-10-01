from collections import namedtuple

Ant = namedtuple('Ant', ['state', 'substate', 'current', 'source'])

def ant():
    return Ant('exploration', 'at-nest', 0, None)
