from collections import namedtuple, defaultdict
from random import random
from pprint import pprint

Ant = namedtuple('Ant', ['state', 'substate', 'current', 'source', 'i', 'delay'])

# Number of nests

def transition(**kwargs):
    def modify(ant):
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

def find_nest(ant):
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

def accept_nest(ant):
    p = nest_acceptances[nest_descriptions[ant.current]]
    if random() < p:
        ant = transition(state='committed')(ant)
        return recruit(ant)
    return ant

def quorum_met(nest):
    return False

# Determine probability of recruiting, and then recruit if over it
def recruit_from(ant):
    p = recruit_probabilities[nest_descriptions[ant.current]]
    if random() < p:
        return recruit(ant)
    return ant

reverse = 0.011

def recruit(ant):
    if quorum_met(ant.current):
        if random() < reverse:
            return transition(state='committed', substate='transport')(ant)
        else:
            return transition(state='committed', substate='reverse-tandem')(ant)
    else:
        return transition(state='canvassing', substate='forward-tandem')(ant)
    return ant

stoptrans = 0.181

def transport(ant):
    if random() < stoptrans:
        return transition(substate='search')(ant)
    else:
        return recruit(ant) # TODO: ????

def reverse_tandem(ant):
    return transition(substate='transport')(ant) # TODO: ?????

def travel(ant):
    # TODO: Delays
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

def update(ant):
    possibilities = states[ant.state][ant.substate]
    for k, v in possibilities.items():
        if isinstance(v, tuple):
            probability, transition = v
            if random() < probability:
                return transition(ant)
        else:
            return v(ant)
    return ant

def count_ants(ants):
    countDict = defaultdict(lambda : 0)
    for ant in ants:
        countDict[(ant.state, ant.substate, ant.current, ant.source)] += 1
    pprint(dict(countDict))

#Ant = namedtuple('Ant', ['state', 'substate', 'current', 'source', 'i', 'delay'])
def main():
    N = 100
    ants = [Ant('assessment', 'at-nest', 0, 0, i, 0)  for i in range(N)]
    while True:
        ants = list(map(update, ants))
        count_ants(ants)

main()
