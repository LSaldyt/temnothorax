from random      import random, choice
from collections import defaultdict
from copy        import deepcopy
from pprint      import pprint
from functools   import reduce
from time        import sleep

import matplotlib.pyplot as plt

class Agent:
    def __init__(self):
        self.commitment = 0.0
        self.current = 0

    def __str__(self):
        return 'ant {}({})'.format(self.current, self.commitment)

    def __repr__(self):
        return str(self)

    def encounter(self, nest, weights):
        self.commitment = weights[nest]
        self.current    = nest

def transform(agents, agent, weights, free):
    if random() < agent.commitment:
        options = list(reduce(set.union, (s for k, s in free.items() if k != agent.current), set()))
        if options:
            # Recruit
            recruited = agents[choice(options)]
            recruited.encounter(agent.current, weights)
    else:
        for j, weight in enumerate(weights):
            if random() < weight:
                agent.encounter(j, weights)
    return agent

def gen_free(agents):
    free = defaultdict(set)
    for i, agent in enumerate(agents):
        free[agent.current].add(i)
    return free

N = 208
weights = [0.0, 0.015, 0.02]
M = len(weights)
agents  = [Agent() for i in range(N)]
free = gen_free(agents)

history = defaultdict(list)

iterations = 100
for i in range(iterations):
    agents = list(transform(agents, agent, weights, free) for agent in agents)
    free = gen_free(agents)
    for k in range(M):
        if k in free:
            history[k].append(len(free[k]))
        else:
            history[k].append(0)

time = list(range(iterations))
linestyles = ['-', '--', '-.']
colors     = ['orange', 'blue', 'green']
for i, H in history.items():
    linestyle = linestyles[i]
    color = colors[i]
    plt.plot(time, H, color=color, label='Nest ' + str(i), linestyle=linestyle)
plt.ylabel('Population count')
plt.xlabel('Timesteps')
plt.legend()
plt.title('Ant populations in feedback-loop model')
plt.show()
