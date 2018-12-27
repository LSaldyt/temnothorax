#!/usr/bin/env python3
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import pandas
import sys, os

from scipy.integrate import odeint

import numpy as np

from collections import defaultdict
sns.set()

# plt.rcParams.update({
#     "lines.color": "white",
#     "patch.edgecolor": "white",
#     "text.color": "black",
#     "axes.facecolor": "white",
#     "axes.edgecolor": "lightgray",
#     "axes.labelcolor": "white",
#     "xtick.color": "white",
#     "ytick.color": "white",
#     "grid.color": "lightgray",
#     "figure.facecolor": "black",
#     "figure.edgecolor": "black",
#     "savefig.facecolor": "black",
#     "savefig.edgecolor": "black"})

# Populations: [S, A, R, P]

T = 10
M = 3
N = 208  # SD 99
p = 0.25 # SD 0.1
final_percentage = 0.95

rho = defaultdict(lambda : 0)
rho[(2, 1)] = 0.008

alpha = [0.0, 0.015, 0.02]
phi = [0.0, 0.13, 0.13]
lambdas = [0.0, 0.033, 0.033]
tau     = 0.001

def unpack(Populations, nestCount):
    S, *rest = Populations
    unpacked = [S, []]
    for i, item in enumerate(rest):
        if i > 0 and i % nestCount == 0:
            unpacked.append([])
        unpacked[-1].append(item)
    return unpacked

def pack(S=0, A=[], R=[], P=[]):
    return [S, *A, *R, *P]

def I(Ri, S):
    return Ri * S
    return Ri if Ri < T and S >= 0 else 0

def dS(Population):
    S, A, R, P = unpack(Population, M)
    return (-sum(phi[i] * S + lambdas[i] * I(R[i], S)
                 for i in range(M)))

def dAi(Population, i):
    S, A, R, P = unpack(Population, M)
    return (phi[i] * S
            + lambdas[i] * I(R[i], S)
            + sum((rho[(j, i)]*A[j] - rho[(i, j)]*A[i])
                  for j in range(len(A)) if j != i)
            - alpha[i]*A[i]
            )

def dRi(Population, i):
    S, A, R, P = unpack(Population, M)
    return (alpha[i]*A[i]
            + sum((rho[(j, i)]*R[j] -  rho[(i, j)]*R[i])
                  for j in range(len(A)) if j != i))

def dPi(Population, i):
    S, A, R, P = unpack(Population, M)
    return sum(tau*P[j]*R[i]
               - tau*P[i]*R[j]
               for j in range(M) if j != i)

def dPopulation_dt(Population, t):
    result =  [ dS(Population)]
    result += [dAi(Population, i) for i in range(M)]
    result += [dRi(Population, i) for i in range(M)]
    result += [dPi(Population, i) for i in range(M)]
    return result

Population0 = pack(S=N*p,
                   A=[0, 0, 0],
                   R=[0, 0, 0],
                   P=[N*(1-p), 0, 0])

N = 1000
intersteps = 10
ts = np.linspace(0, N, N * intersteps)
Ps = odeint(dPopulation_dt, Population0, ts)
for do_passive in [True, False]:
    for i in range(1 + M * 3):
        if i == 0:
            label = 'Searching'
        else:
            label = ['Assessing', 'Recruiting', 'Passive'][(i - 1) // M]
            label += '_' + str((i - 1) % M)
        pop = Ps[:,i]
        if do_passive:
            if 'Passive' in label:
                plt.plot(ts, pop, label=label)
        else:
            if 'Passive' not in label and (i - 1) % M != 0:
                plt.plot(ts, pop, label=label)

    plt.legend(loc='center right', bbox_to_anchor=(1, 0.5))
    plt.xlabel('Timesteps')
    plt.ylabel('Population count')
    plt.title('Population dynamics during decision process')
    filename = ('passive' if do_passive else 'active') + '_populations_pratt_2002.png'
    plt.savefig(filename)
    plt.show()
