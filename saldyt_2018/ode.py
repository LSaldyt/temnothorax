#!/usr/bin/env python3
import matplotlib.pyplot as plt

# SPratt Parameters from 2002 paper
N = 208  # SD 99
p = 0.25 # SD 0.1
M = 3
T = 10
final_percentage = 0.95

# From Granivoskiy 2012
# SearchE = 0.0191
# SearchA = 0.0195
# SearchC(L) = 0.018
# SearchC(C) = 0.0044

sigmaA  = [0.0, 0.0195, 0.0195]
sigmaL  = [0.0, 0.018,  0.018]
sigmaC  = [0.0, 0.0044, 0.0044]
sigmaA  = [0.0, 0.0,    0.0]
sigmaL  = [0.0, 0.0,    0.0]
sigmaC  = [0.0, 0.0,    0.0]
lambdas = [0.0, 0.033, 0.033]
alpha   = [0.0, 0.015, 0.02]
#tau    = [0.001, 0.001, 0.001] # 0.99 technically.. artificially lowered
tau     = 0.001
phi     = [0.0, 0.13, 0.13]

S = int(p * N)
C = [0] * M
A = [0] * M
L = [0] * M
P = [int((1 - p) * N)] + [0] * (M - 1)

def dS():
    return S * sum(
        - phi[i]
        - lambdas[i] * L[i]
        - tau * C[i]
        + sigmaA[i] * A[i]
        + sigmaL[i] * L[i]
        + sigmaC[i] * C[i]
        for i in range(M))

def dAi(i):
    return (S * (phi[i]
            + lambdas[i] * L[i]
            + tau * C[i]
            - sigmaA[i] * A[i])
            - alpha[i] * A[i]
            + sum(+ tau * C[i] * A[j]
                  + tau * C[i] * L[j]
                  + tau * C[i] * C[j]
                  - tau * C[j] * A[i]
                for j in range(M) if j != i))

def Q(i):
    return int(A[i] + L[i] + C[i] >= T)
    #return int(A[i] + L[i] + C[i] + P[i] > T)

def dLi(i):
    return (alpha[i] * A[i]
           - Q(i)*L[i]
           - sigmaL[i] * L[i]
           - sum(tau*C[j]*L[i]
               for j in range(M) if j != i))

def dCi(i):
    return (Q(i) * L[i] - sigmaC[i] * C[i] - sum(tau*C[j]*C[i] for j in range(M) if j != i))

def dPi(i):
    return sum(tau*P[j]*C[i]
               - tau*P[i]*C[j]
               for j in range(M) if j != i)

S_history = []
C_history = []
A_history = []
L_history = []
P_history = []

iterations = 200000
done = False
for i in range(iterations):
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
    for nestP in P[1:]:
        if nestP > final_percentage * N * (1-p):
            done = True
    if done:
        iterations = i + 1
        break
print('Performed {} iterations'.format(iterations))

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

