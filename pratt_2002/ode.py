import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('whitegrid')

# SPratt Parameters from 2002 paper
N = 208  # SD 99
p = 0.25 # SD 0.1
M = 2
l   = [0.033] * M # SD 0.016
phi = [0.099] * M # SD 0.02
u   = [0.013] * M # SD 0.006
k   = [0.015, 0.02] # SD 0.006 and 0.008 respectively

rho = {
    (0, 1) : 0.008, # SD 0.004
    (1, 0) : 0.0
}

#c = 4.6 # Minutes to move item.. not used
T = 100 # ?

def I(Ri, S):
    return Ri if Ri < T and S > 0 else 0

def J(Ri, Pinitial):
    return 0 if Ri < T or Pinitial == 0 else Ri

def dS(S, R):
    return (-sum(ui * S for ui in u)
            - sum(l[i] * I(R[i], S) for i in range(len(R))))

def dAi(S, R, A, i):
    return (u[i] * S
            + l[i] * I(R[i], S)
            + sum((rho[(i, j)]*A[j] -  rho[(j, i)]*A[i])
                  for j in range(len(A)) if j != i)
            - k[i]*A[i]
            )

def dRi(R, A, i):
    return (k[i]*A[i]
            + sum((rho[(j, i)]*R[j] -  rho[(i, j)]*R[i])
                  for j in range(len(A)) if j != i))

def dPi(R, Pinitial, i):
    print('dPi debug:')
    print(phi[i] * J(R[i], Pinitial))
    print(J(R[i], Pinitial))
    return phi[i] * J(R[i], Pinitial)

def simulate():
    S = int(p * N)
    Pinitial = int((1.0 - p) * N)
    P = [0] * M
    A = [0] * M
    R = [0] * M

    S_history = []
    P_history = []
    A_history = []
    R_history = []

    print('Initial Population:')
    print('S: {S}\nA: {A}\nR: {R}\nP: {P}'.format(S=S, A=A, R=R, P=P))
    #iterations = 143
    iterations = 1000
    for _ in range(iterations):
        S_history.append(S)
        P_history.append(P)
        A_history.append(A)
        R_history.append(R)

        newS = S + dS(S, R)
        newA = [Ai + dAi(S, R, A, i)     for i, Ai in enumerate(A)]
        newR = [Ri + dRi(R, A, i)        for i, Ri in enumerate(R)]
        newP = [Pi + dPi(R, Pinitial, i) for i, Pi in enumerate(P)]
        S = newS #round(newS)
        A = newA # list(map(round, newA))
        R = newR # list(map(round, newR))
        P = newP # list(map(round, newP))
        print('Population:')
        print('S: {S}\nA: {A}\nR: {R}\nP: {P}'.format(S=S, A=A, R=R, P=P))

    time = list(range(iterations))
    plt.plot(time, [N] * iterations, color='black', alpha=0.5, label='Total ant limit')
    plt.plot(time, [int(N*p)] * iterations, '--', color='black', alpha=0.5, label='Active ant limit')
    #plt.plot(time, [int(N*(1.0 - p))] * iterations, color='black', alpha=0.5, label='Passive ant limit')
    plt.plot(time, S_history, label='Searching')
    for i, Ah in enumerate(zip(*A_history)):
        linestyle = ['-', '--'][i]
        plt.plot(time, Ah, color='purple', label='Assessment {}'.format(i), linestyle=linestyle)
    for i, Rh in enumerate(zip(*R_history)):
        linestyle = ['-', '--'][i]
        plt.plot(time, Rh, color='orange', label='Recruitment {}'.format(i), linestyle=linestyle)
    for i, Ph in enumerate(zip(*P_history)):
        linestyle = ['-', '--'][i]
        plt.plot(time, Ph, color='green', label='Passive {}'.format(i), linestyle=linestyle)
    plt.legend()
    plt.xlabel('Minutes')
    plt.ylabel('Population count')
    plt.title('Population dynamics during nest search for Temnothorax')
    plt.show()

if __name__ == '__main__':
    simulate()
