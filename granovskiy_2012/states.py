from collections import namedtuple, defaultdict
from random import random
from pprint import pprint
from copy import deepcopy

from plot import plot

Ant = namedtuple('Ant', ['state', 'substate', 'current', 'source', 'i', 'delay', 'delay_task'])

# Number of nests
def transition(**kwargs):
    def modify(ant, stateLookup=None, nestLookup=None):
        return ant._replace(**kwargs)
    return modify

nest_descriptions = {0 : 'destroyed',
                     1 : 'mediocre',
                     2 : 'good'}

M = len(nest_descriptions)

nest_acceptances      = {'good' : 0.0056, 'mediocre' : 0.0023, 'destroyed' : 0.0}
recruit_probabilities = {'good' : 0.0289, 'mediocre' : 0.0238, 'destroyed' : 0.0}

def get_nest_find_rate(at, to):
    if at == 0:
        if to == 0:
            return 0.0073
        else:
            return 0.001
    elif at == to:
        return 0.0108
    else:
        return 0.001

def find_nest(ant, stateLookup, nestLookup):
    # Depending on source and current nest, make probabilistic transition
    at = ant.current
    for i in range(M):
        p = get_nest_find_rate(at, i)
        if random() < p:
            change = dict(substate='at-nest', current=i, source=i)
            if i == at:
                change['state'] = 'assessment' # Change to assessment if visiting a novel nest
            return transition(**change)(ant)
    return ant

def accept_nest(ant, stateLookup, nestLookup):
    p = nest_acceptances[nest_descriptions[ant.current]]
    if random() < p:
        ant = transition(state='committed')(ant)
        return recruit(ant, stateLookup, nestLookup)
    return ant

def quorum_met(nest, stateLookup, nestLookup):
    return False

# Determine probability of recruiting, and then recruit if over it
def recruit_from(ant, stateLookup, nestLookup):
    p = recruit_probabilities[nest_descriptions[ant.current]]
    if random() < p:
        return recruit(ant, stateLookup, nestLookup)
    return ant

reverse = 0.011

def recruit(ant, stateLookup, nestLookup):
    if quorum_met(ant.current, stateLookup, nestLookup):
        if random() < reverse:
            return transition(state='committed', substate='transport')(ant)
        else:
            return transition(state='committed', substate='reverse-tandem')(ant)
    else:
        return transition(state='canvassing', substate='forward-tandem')(ant)
    return ant

stoptrans = 0.181

def transport(ant, stateLookup, nestLookup):
    if random() < stoptrans:
        return transition(substate='search')(ant)
    else:
        return recruit(ant, stateLookup, nestLookup) # TODO: ????

def reverse_tandem(ant, stateLookup, nestLookup):
    return transition(substate='transport')(ant) # TODO: ?????

def travel(ant, stateLookup, nestLookup):
    return transition(state='canvassing', substate='at-nest')(ant) # TODO: ?????

# Values are either custom functions or tuples describing probability transitions

states = {
    'exploration' : {
        'search' : {
            'find' : find_nest
            },
        'at-nest' : {
            'search-explore' : (0.0191, transition(substate='search')),
            }
        },
    'assessment'  : {
        'search' : {
            'find' : find_nest
            },
        'at-nest' : {
            'search-assess' : (0.0195, transition(substate='search')),
            'accept' : accept_nest
            }
        },
    'canvassing'  : {
        'search' : {
            'find' : find_nest
            },
        'at-nest' : {
            'search-canvassing' : (0.018, transition(substate='search')),
            'recruit' : recruit_from
            },
        'forward-tandem' : {
            'travel' : travel
            # Delay.. then go to at-nest
            }
        },
    'committed' : {
        'search' : {
            'find' : find_nest,
            },
        'at-nest' : {
            'search-committed' : (0.0044, transition(substate='search')),
            'recruit' : recruit
            },
        'transport' : {
            'transport' : transport
            },
        'reverse-tandem' : {
            'reverse-tandem' : reverse_tandem
            }
        }
}

def update(ant, stateLookup, nestLookup):
    stateLookup[ant.state][ant.substate].remove(ant.i)
    nestLookup[ant.current].remove(ant.i)
    if ant.delay == 1:
        return ant.delay_task(ant._replace(delay=0))
    elif ant.delay > 0:
        return ant._replace(delay=ant.delay - 1)
    possibilities = states[ant.state][ant.substate]
    for k, v in possibilities.items():
        if isinstance(v, tuple):
            probability, transition = v
            if random() < probability:
                ant = transition(ant, stateLookup, nestLookup)
                break
        else:
            ant = v(ant, stateLookup, nestLookup)
            break
    stateLookup[ant.state][ant.substate].add(ant.i)
    nestLookup[ant.current].add(ant.i)
    return ant

def main():
    N = 100
    iterations = 5000
    stateLookup = defaultdict(lambda : defaultdict(set))
    nestLookup = {i : set() for i in range(M)}
    ants = [Ant('assessment', 'at-nest', 0, 0, i, 0, None)  for i in range(N)]
    for ant in ants:
        stateLookup[ant.state][ant.substate].add(ant.i)
        nestLookup[ant.current].add(ant.i)
    history = []
    for _ in range(iterations):
        ants = list(map(lambda a : update(a, stateLookup, nestLookup), ants))
        history.append({k : len(v) for k, v in nestLookup.items()})
    plot(history)

main()
