from random      import random, choice
from collections import defaultdict
from copy        import deepcopy
from pprint      import pprint
from functools   import reduce
from time        import sleep

import pandas
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('darkgrid')

#plt.rcParams.update({
#    "lines.color": "white",
#    "patch.edgecolor": "white",
#    "text.color": "black",
#    "axes.facecolor": "white",
#    "axes.edgecolor": "lightgray",
#    "axes.labelcolor": "white",
#    "xtick.color": "white",
#    "ytick.color": "white",
#    "grid.color": "lightgray",
#    "figure.facecolor": "black",
#    "figure.edgecolor": "black",
#    "savefig.facecolor": "black",
#    "savefig.edgecolor": "black"})

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

def simulate(N, weights, phi, plot=False, iterations=500):
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
        plt.savefig('agent_based_population_model.png')
        plt.show()
    return iterations

data = defaultdict(list)

Ns = [208]
#alphas = np.linspace(0.0, 0.1, 50)
#alphas = np.linspace(0.0, 1.0, 50)
#alphas = np.linspace(0.0, 1.0, 10)
alphas = [0.015]
#betas  = alphas
betas  = [0.02]
phis   = [0.013]
phis   = np.linspace(0.0, 0.1, 31)

#simulate(208, [0.0, 0.015, 0.02, 0.03], [0.0, 0.013, 0.013, 0.013], True, iterations=5000)
#simulate(1000, [0.0, 0.015, 0.015, 0.015], [0.0, 0.013, 0.013, 0.013], True, iterations=1000)
#simulate(1000, [0.0, 0.3, 0.25, 0.9], [0.0, 0.1, 0.1, 0.05], True, iterations=1000)
for N in Ns:
    for alpha in alphas:
        for beta in betas:
            for phi_a in phis:
                for phi_b in phis:
                    add = lambda k, v : data[k].append(round(v, 4))
                    data['N'].append(N)
                    add('alpha', alpha)
                    add('beta', beta)
                    add('phi_a', phi_a)
                    add('phi_b', phi_b)
                    weights = [0.0, alpha, beta]
                    phi     = [0.0, phi_a, phi_b]
                    data['iterations'].append(simulate(N, weights, phi, iterations=1000))

#print(data)
original_data = pandas.DataFrame(data)
print(original_data)
#data = original_data.pivot_table(values='iterations', index='beta', columns=['alpha'])
#sns.heatmap(data, yticklabels=True, xticklabels=True)
#plt.title('Convergence times for nest quality and threshold')
#plt.xlabel('Alpha')
#plt.ylabel('Beta')
#plt.savefig('agent_convergence_times.png')
#plt.show()
data = original_data.pivot_table(values='iterations', index='phi_b', columns=['phi_a'])
sns.heatmap(data)#, yticklabels=True)
plt.title('Convergence times for nest quality and threshold')
plt.xlabel('Phi_a')
plt.ylabel('Phi_b')
plt.savefig('distance_agent_convergence_times.png')
plt.show()
