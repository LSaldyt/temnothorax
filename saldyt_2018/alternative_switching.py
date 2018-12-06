#!/usr/bin/env python3
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import pandas
import sys, os

from scipy.integrate import odeint

import numpy as np

from collections import defaultdict

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

#alpha = [0.0, 0.015, 0.02]
phi = [0.0, 0.13, 0.13]
sigmaA  = [0.0, 0.0195, 0.0195]
sigmaL  = [0.0, 0.018,  0.018]
sigmaC  = [0.0, 0.044,  0.044]
#sigmaA  = [0.0, 0.0,   0.0]
#sigmaL  = [0.0, 0.0,   0.0]
#sigmaC  = [0.0, 0.0,   0.0]
lambdas = [0.0, 0.033, 0.033]
tau     = 0.001

def simulate(N, alpha, phi, iterations=1000, plot=False, quorum_convergence=False):
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
        return int(L[i] + C[i] >= T)
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

    converged = iterations
    intersteps = 10
    ts = np.linspace(0, iterations, iterations * intersteps)
    Ps = odeint(dPopulation_dt, Population0, ts)
    for do_passive in [True, False]:
        for i in range(1 + M * 4):
            if i == 0:
                label = 'Searching'
            else:
                label = ['Assessing', 'Leading', 'Carrying', 'Passive'][(i - 1) // M]
                index = (i - 1) % M
                label += '_' + str(index)
            pop = Ps[:,i]
            if quorum_convergence:
                converge_label = 'Carrying'
                converge_condition = lambda x : x > 0
            else:
                converge_label = 'Passive'
                converge_condition = lambda x : x > N*(1-p)*.95
            if converge_label in label and index > 0:
                early_converged = [(i, x) for i, x in enumerate(pop) if converge_condition(x)]
                if early_converged:
                    converged = min(early_converged, key=lambda t : t[0])[0] / intersteps
            if do_passive:
                if 'Passive' in label and plot:
                    plt.plot(ts, pop, label=label)
            else:
                if 'Passive' not in label and plot:
                    plt.plot(ts, pop, label=label)
        if plot:
            plt.legend(loc='center right', bbox_to_anchor=(1, 0.5))
            plt.xlabel('Timesteps')
            plt.ylabel('Population count')
            plt.title('Population dynamics during decision process')
            filename = ('passive' if do_passive else 'active') + '_populations_saldyt_2018_alt.png'
            plt.savefig(filename)
            plt.show()
    return converged

#print(simulate(True, True))

data = defaultdict(list)

Ns = [208]
#alphas = np.linspace(0.0, 0.1, 50)
#alphas = np.linspace(0.0, 1.0, 50)
alphas = np.linspace(0.0, 1.0, 31)
#alphas = [0.015]
betas  = alphas
#betas  = [0.02]
phis   = [0.013]
#phis   = np.linspace(0.0, 0.1, 21)

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
                    data['iterations'].append(simulate(N, weights, phi, iterations=400))

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
data = original_data.pivot_table(values='iterations', index='alpha', columns=['beta'])
sns.heatmap(data)#, yticklabels=True)
plt.title('Convergence times for nest quality and threshold')
plt.xlabel('alpha')
plt.ylabel('beta')
plt.savefig('quality_ode_convergence_times.png')
plt.show()
