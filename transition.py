from functools import wraps
import random

from ant import Ant
from parameters import parameters


def transition(**kwargs):
    for key in kwargs:
        assert key in Ant._fields, 'Invalid transition key: {}'.format(key)
    def modifier(ant):
        return ant._replace(**kwargs)
    return modifier

def move(i):
    def modifier(ant):
        ant = ant._replace(source=ant.current)
        ant = ant._replace(current=i)
        return ant
    return modifier

def move_random(ant):
    i = random.randint(1, parameters['__nest_count__'])
    return move(i)(ant)

