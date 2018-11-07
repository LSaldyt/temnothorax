from collections import namedtuple, defaultdict
from functools import wraps
from random import random, choice
from pprint import pprint
from copy import deepcopy

from plot import plot

Ant = namedtuple('Ant', ['state', 'substate', 'current', 'source', 'i', 'delay', 'delay_task'])

def modifies_lookups(f):
    @wraps(f)
    def inner(ant, ants, stateLookup, nestLookup):
        try:
            stateLookup[ant.state][ant.substate].remove(ant.i)
        except KeyError:
            print(ant, ants, stateLookup, nestLookup)
            print(ant.state)
            print(ant.substate)
        try:
            nestLookup[ant.current].remove(ant.i)
        except KeyError:
            print(ant, ants, stateLookup, nestLookup)
            print(ant.current)
        ant = f(ant, ants, stateLookup, nestLookup)
        stateLookup[ant.state][ant.substate].add(ant.i)
        nestLookup[ant.current].add(ant.i)
        return ant
    return inner

def transition(**kwargs):
    @modifies_lookups
    def modify(ant, ants=None, stateLookup=None, nestLookup=None):
        return ant._replace(**kwargs)
    return modify

# Define the nests to be simulated. This simulates an original destroyed nest, and two nests to choose from: one good and one mediocre
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

def find_nest(ant, ants, stateLookup, nestLookup):
    # Depending on source and current nest, make probabilistic transition
    at = ant.current
    for i in range(M):
        p = get_nest_find_rate(at, i)
        if random() < p:
            change = dict(substate='at-nest', current=i)
            if i == at:
                change['state'] = 'assessment' # Change to assessment if visiting a novel nest
            return transition(**change)(ant, ants, stateLookup, nestLookup)
    return ant

def accept_nest(ant, ants, stateLookup, nestLookup):
    p = nest_acceptances[nest_descriptions[ant.current]]
    if random() < p:
        ant = transition(state='committed')(ant, ants, stateLookup, nestLookup)
        return recruit(ant, ants, stateLookup, nestLookup)
    return ant

T = 8

def quorum_met(nest, ants, stateLookup, nestLookup):
    return len(nestLookup[nest]) > T

# Determine probability of recruiting, and then recruit if over it
def recruit_from(ant, ants, stateLookup, nestLookup):
    p = recruit_probabilities[nest_descriptions[ant.current]]
    if random() < p:
        return recruit(ant, ants, stateLookup, nestLookup)
    return ant

reverse = 0.011

stoptrans = 0.181

def select_ant(stateLookup):
    possible = set()
    state    = choice(list(stateLookup.keys()))
    for substate in ['at-nest', 'search']:
        possible.update(stateLookup[state][substate])
    return choice(list(possible))

@modifies_lookups
def recruit(ant, ants, stateLookup, nestLookup):
    if quorum_met(ant.current, ants, stateLookup, nestLookup):
        if random() < reverse:
            return transition(state='committed', substate='transport')(ant, ants, stateLookup, nestLookup)
        else:
            return transition(state='committed', substate='reverse-tandem')(ant, ants, stateLookup, nestLookup)
    else:
        return transition(state='canvassing', substate='forward-tandem')(ant, ants, stateLookup, nestLookup)
    return ant


transport_delay_time = 10

@modifies_lookups
def transport(ant, ants, stateLookup, nestLookup):
    if random() < stoptrans:
        return transition(substate='search')(ant, ants, stateLookup, nestLookup)
    else:
        peers = list(nestLookup[ant.source])
        if len(peers) != 0:
            selected = choice(peers)
            selectedAnt = ants[selected]
            delay_task = transition(state='assessment', substate='at-nest', current=ant.current, source=ant.current)
            ants[selected] = selectedAnt._replace(state='carried', substate='carried', delay=transport_delay_time, delay_task=delay_task)
            ant = ant._replace(delay=transport_delay_time, delay_task=transition(substate='recruit'))
        return ant

@modifies_lookups
def reverse_tandem(ant, ants, stateLookup, nestLookup):
    # TODO: Reverse tandem run here
    # delay_task = transition(substate='transport')(ant, ants, stateLookup, nestLookup) # TODO: ?????
    return ant

tandem_delay_time = 10

@modifies_lookups
def forward_tandem(ant, ants, stateLookup, nestLookup):
    # TODO: Tandem run here
    peers = list(nestLookup[ant.source])
    if len(peers) != 0:
        selected = choice(peers)
        print(selected)
        print('Number of ants:')
        print(len(ants))
        selectedAnt = ants[selected]
        print(selectedAnt)
        delay_task = transition(state='assessment', substate='at-nest', current=ant.current, source=ant.current)
        ants[selected] = selectedAnt._replace(state='following', substate='following', delay=tandem_delay_time, delay_task=delay_task)
        ant = ant._replace(delay=transport_delay_time, delay_task=transition(state='canvassing', substate='at-nest'))
    return ant

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
            'forward_tandem' : forward_tandem
            },
        'recruit' : {
            'recruit' : recruit
            }
        },
    'committed' : {
        'search' : {
            'find' : find_nest,
            },
        'recruit' : {
            'recruit' : recruit
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
        },
    'following' : {'following' : {}},
    'carried' : {'carried' : {}}
}

#@modifies_lookups
def update(ant, ants, stateLookup, nestLookup):
    if ant.delay == 1:
        ant = ant._replace(delay=0)
        if ant.delay_task is not None:
            ant = ant.delay_task(ant, ants, stateLookup, nestLookup)._replace(delay_task=None)
    elif ant.delay > 0:
        ant = ant._replace(delay=ant.delay - 1)
    else:
        try:
            possibilities = states[ant.state][ant.substate]
        except KeyError:
            print(ant.state)
            print(ant.substate)
            raise
        for k, v in possibilities.items():
            if isinstance(v, tuple):
                probability, transition = v
                if random() < probability:
                    ant = transition(ant, ants, stateLookup, nestLookup)
                    break
            else:
                ant = v(ant, ants, stateLookup, nestLookup)
                break
    return ant

def main():
    N = 100
    iterations = 10000
    stateLookup = defaultdict(lambda : defaultdict(set))
    nestLookup = {i : set() for i in range(M)}
    ants = [Ant('assessment', 'at-nest', 0, 0, i, 0, None)  for i in range(N)]
    for ant in ants:
        stateLookup[ant.state][ant.substate].add(ant.i)
        nestLookup[ant.current].add(ant.i)
    history = []
    taskHistory = []
    for _ in range(iterations):
        ants = list(map(lambda a : update(a, ants, stateLookup, nestLookup), ants))
        history.append({k : len(v) for k, v in nestLookup.items()})
        taskDict = {k1 + '-' + k2 : len(v2) for k1, v1 in stateLookup.items() for k2, v2 in v1.items()}
        taskDict.update({k1 + '-' + k2 : 0 for k1, v1 in states.items() for k2 in v1 if (k1 + '-' + k2) not in taskDict})
        taskHistory.append(taskDict)
    plot(history)
    plot(taskHistory)

main()
