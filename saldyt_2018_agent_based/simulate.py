#!/usr/bin/env python3
from random      import random, choice
from collections import defaultdict
from copy        import deepcopy
from pprint      import pprint
from functools   import reduce
from time        import sleep

import sys
import pandas
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('darkgrid')

from agent import Agent

def transform(agents, agent, weights, phi, free):
    if random() < agent.commitment:
        options = list(reduce(set.union, (s for k, s in free.items() if k != agent.current), set()))
        if options:
            recruited = agents[choice(options)]
            recruited.encounter(agent.current, weights)
    else:
        for j, p in enumerate(phi):
            if random() < p:
                agent.encounter(j, phi)
    return agent

def gen_free(agents):
    free = defaultdict(set)
    for i, agent in enumerate(agents):
        free[agent.current].add(i)
    return free

def simulate(N, weights, phi, plot=False, iterations=500, plot_title='agent_based_populations.png', show=False):
    linestyles = ['-', '--', '-.'] * 100
    colors     = ['orange', '#1357c4', 'purple', 'green']
    M = len(weights)
    agents  = [Agent() for i in range(N)]
    free = gen_free(agents)

    history = defaultdict(list)

    done = False
    for i in range(iterations):
        if done:
            iterations = i
            break
        agents = list(transform(agents, agent, weights, phi, free) for agent in agents)
        free = gen_free(agents)
        for k in range(M):
            if k != 0 and len(free[k]) > .9 * N:
                done = True
            if k in free:
                history[k].append(len(free[k]))
            else:
                history[k].append(0)

    if plot:
        time = list(range(iterations))
        for i, H in history.items():
            linestyle = linestyles[i]
            color = colors[i]
            plt.plot(time, H, color=color, label='Nest ' + str(i), linestyle=linestyle)
        plt.ylabel('Population count')
        plt.xlabel('Timesteps')
        plt.legend()
        plt.title('Ant populations in feedback-loop model')
        plt.savefig(plot_title)
        if show:
            plt.show()
        else:
            plt.clf()
    return iterations

def main(args):
    simulate(208, [0.0, 0.015, 0.015], [0.0, 0.013, 0.013], True, iterations=1000, plot_title='similar.png')
    simulate(208, [0.0, 0.015, 0.02], [0.0, 0.013, 0.013], True, iterations=5000, plot_title='original.png')
    simulate(208, [0.0, 0.015, 0.02, 0.03], [0.0, 0.013, 0.013, 0.013], True, iterations=5000, plot_title='tri.png')
    simulate(1000, [0.0, 0.015, 0.02], [0.0, 0.013, 0.013], True, iterations=5000, plot_title='original_1k.png')
    simulate(1000, [0.0, 0.015, 0.02, 0.03], [0.0, 0.013, 0.013, 0.013], True, iterations=5000, plot_title='tri_1k.png')
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
