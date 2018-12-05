#!/usr/bin/env python3
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import pandas
import sys, os

from scipy.integrate import odeint

import numpy as np

from collections import defaultdict

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

# From Granivoskiy 2012
# SearchE = 0.0191
# SearchA = 0.0195
# SearchC(L) = 0.018
# SearchC(C) = 0.0044

alpha = [0.0, 0.015, 0.02]
phi = [0.0, 0.13, 0.13]
sigmaA  = [0.0, 0.0195, 0.0195]
sigmaL  = [0.0, 0.018,  0.018]
sigmaC  = [0.0, 0.044,  0.044]
#sigmaA  = [0.0, 0.0,   0.0]
#sigmaL  = [0.0, 0.0,   0.0]
#sigmaC  = [0.0, 0.0,   0.0]
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

def pack(S=0, A=[], L=[], C=[], P=[]):
    return [S, *A, *L, *C, *P]

def Q(Population, i):
    S, A, L, C, P = unpack(Population, M)
    return int(A[i] + L[i] + C[i] >= T)
    #return int(A[i] + L[i] + C[i] + P[i] > T)

def dS(Population):
    S, A, L, C, P = unpack(Population, M)
    return (-sum(phi[i] * S + lambdas[i] * L[i] * S
                 - tau * C[i] * S
                 for i in range(M)))

def dAi(Population, i):
    S, A, L, C, P = unpack(Population, M)
    return (phi[i] * S
            + lambdas[i] * L[i] * S

            + sum(tau * (C[i] * (S +
                                 L[j] +
                                 C[j] +
                                 A[j])
                       - C[j] * A[i])
                  for j in range(len(A)) if j != i)
            - alpha[i]*A[i]
            )

def dLi(Population, i):
    S, A, L, C, P = unpack(Population, M)
    return (- sigmaL[i] * L[i] +
           (alpha[i] * A[i]
           - Q(Population, i)*L[i]
           - sum(tau*C[j]*L[i] for j in range(M) if j != i)
           ))

def dCi(Population, i):
    S, A, L, C, P = unpack(Population, M)
    return (Q(Population, i) * L[i] #- sigmaC[i] * C[i] -
               - sum(tau*C[j]*C[i] for j in range(M) if j != i)
               )

def dPi(Population, i):
    S, A, L, C, P = unpack(Population, M)
    return sum(tau*P[j]*C[i]
               - tau*P[i]*C[j]
               for j in range(M) if j != i)

def dPopulation_dt(Population, t):
    result =  [ dS(Population)]
    result += [dAi(Population, i) for i in range(M)]
    result += [dLi(Population, i) for i in range(M)]
    result += [dCi(Population, i) for i in range(M)]
    result += [dPi(Population, i) for i in range(M)]
    return result

Population0 = pack(S=N*p,
                   A=[0, 0, 0],
                   L=[0, 0, 0],
                   C=[0, 0, 0],
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
            if 'Passive' not in label:
                plt.plot(ts, pop, label=label)

    plt.legend(loc='center right', bbox_to_anchor=(1, 0.5))
    plt.xlabel('Timesteps')
    plt.ylabel('Population count')
    plt.title('Population dynamics during decision process')
    filename = ('passive' if do_passive else 'active') + '_populations_saldyt_2018_alt.png'
    plt.savefig(filename)
    plt.show()
