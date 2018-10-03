import random, time
from numpy.random import multinomial
from parameters import index_parameter
#def index_parameter(parameters, p, state):

def normalize(l):
    return [x/sum(l) for x in l]

def update(states, parameters, ant):
    probdict = states[ant.state][ant.substate]
    options  = list(probdict.items())
    if len(options):
        weights      = [index_parameter(parameters, k, ant.state)[0] for k, v in options]
        transitions  = [v for k, v in options]

        transition = random.choices(transitions, weights)[0]
        return transition(ant)
    else:
        print('Warning: No available transitions for ant {}'.format(ant))
        return ant
