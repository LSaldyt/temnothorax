#!/usr/bin/env python3
import matplotlib.pyplot as plt

# SPratt Parameters from 2002 paper
N = 208  # SD 99
p = 0.25 # SD 0.1
M = 3
T = 10

# From Granivoskiy 2012
# SearchE = 0.0191
# SearchA = 0.0195
# SearchC(L) = 0.018
# SearchC(C) = 0.0044

sigmaA  = [0.0, 0.0195, 0.0195]
sigmaL  = [0.0, 0.018, 0.018]
sigmaC  = [0.0, 0.0044, 0.0044]
sigmaA  = [0.0, 0.0, 0.0]
sigmaL  = [0.0, 0.0, 0.0]
sigmaC  = [0.0, 0.0, 0.0]
lambdas = [0.0, 0.033, 0.033]
alpha   = [0.0, 0.015, 0.02]
alpha   = [0.0, 0.015, 1.0]
tauP    = [0.001, 0.001, 0.001] # 0.99 technically.. artificially lowered
tauS    = [0.0, 0.001, 0.001]
tauL    = [0.0, 0.001, 0.001]
tauC    = [0.0, 0.001, 0.001]
tauA    = [0.0, 0.001, 0.001]
phi     = [0.0, 0.13, 0.13]
#k   = [0.015, 0.02] # SD 0.006 and 0.008 respectively

S = int(p * N)
C = [0] * M
A = [0] * M
L = [0] * M
P = [int((1 - p) * N)] + [0] * (M - 1)

def dS():
    return sum(
        - phi[i] * S
        - lambdas[i] * min(L[i], S)
        - tauS[i]*min(C[i], S)
        + sigmaA[i] * A[i]
        + sigmaL[i] * L[i]
        + sigmaC[i] * C[i]
        for i in range(M))

def dAi(i):
    return (phi[i] * S
            + lambdas[i] * min(L[i], S)
            + tauS[i] * min(C[i], S)
            - sigmaA[i] * A[i]
            - sigmaL[i] * L[i]
            - sigmaC[i] * C[i]
            - alpha[i] * A[i]
            + sum(tauL[i]*min(L[j], C[i])
                + tauC[i]*min(C[j], C[i])
                + tauA[i]*min(A[j], C[i])
                - tauA[j]*min(P[i], C[j])
                for j in range(M) if j != i))

def Q(i):
    return int(A[i] + L[i] >= T)
    #return int(A[i] + L[i] + C[i] + P[i] > T)

def dLi(i):
    return ((1 - Q(i)) * alpha[i] * A[i]
           - Q(i)*L[i]
           # Re-add later?
           #+ (1 - Q(i)) * C[i]
           + sum(- tauL[j]*min(L[i], C[j])
               for j in range(M) if j != i)
           - sigmaL[i] * L[i])

def dCi(i):
    return (Q(i) * alpha[i] * A[i]
           # Re-add later?
            #- (1 - Q(i)) * C[i]
            + Q(i) * L[i]
            + sum(- tauC[j]*min(C[i], C[j])
                for j in range(M) if j != i)
            - sigmaC[i] * C[i])

def dPi(i):
    return sum(tauP[i]*min(P[j], C[i])
               - tauP[j]*min(P[i], C[j])
               for j in range(M) if j != i)

S_history = []
C_history = []
A_history = []
L_history = []
P_history = []

iterations = 1000
iterations = 10000
for _ in range(iterations):
    S_history.append(S)
    C_history.append(C)
    A_history.append(A)
    L_history.append(L)
    P_history.append(P)

    newS = max(0, S + dS())
    newC = [max(0, Ci + dCi(i)) for i, Ci in enumerate(C)]
    newA = [max(0, Ai + dAi(i)) for i, Ai in enumerate(A)]
    newL = [max(0, Li + dLi(i)) for i, Li in enumerate(L)]
    newP = [max(0, Pi + dPi(i)) for i, Pi in enumerate(P)]
    S = newS
    C = newC
    A = newA
    L = newL
    P = newP
    #print('Population:')
    #print('S: {S}\nA: {A}\nR: {R}\nP: {P}'.format(S=S, A=A, R=R, P=P))
    #print(Pinitial)

time = list(range(iterations))
plt.plot(time, [N] * iterations, color='black', alpha=0.5, label='Total ant limit')
plt.plot(time, [int(N*p)] * iterations, '--', color='black', alpha=0.5, label='Active ant limit')
plt.plot(time, [int(N*(1.0 - p))] * iterations, color='black', alpha=0.5, label='Passive ant limit')
plt.plot(time, S_history, label='Searching')
def show_pop(history, color, label):
    for i, H in enumerate(zip(*history)):
        linestyle = ['-', '--', '-.'][i]
        plt.plot(time, H, color=color, label=label + ' ' + str(i), linestyle=linestyle)
show_pop(A_history, 'red',    'Assessment')
show_pop(C_history, 'purple', 'Carrying')
show_pop(L_history, 'orange', 'Leading')
show_pop(P_history, 'blue',   'Passive')
plt.legend()
plt.show()

