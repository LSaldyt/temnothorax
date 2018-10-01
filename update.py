import random, time
from numpy.random import multinomial

def normalize(l):
    return [x/sum(l) for x in l]

def update(states, parameters, ant):
    probdict = states[ant.state][ant.substate]
    options  = list(probdict.items())
    weights      = [parameters[k][0] for k, v in options]
    transitions  = [v for k, v in options]

    transition = random.choices(transitions, weights)[0]
    print(ant)
    ant = transition(ant)
    print(ant)
    1/0
