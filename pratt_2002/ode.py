# SPratt Parameters from 2002 paper
N = 208 # SD 99
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
T = 20 # ?

def I(Ri, S):
    return Ri if Ri < T and S > 0 else 0

def J(Ri, Pinitial):
    return 0 if Ri < T or Pinitial == 0 else Ri

def dS(S, R):
    return (-sum(ui * S for ui in u)
            + sum(l[i] * I(R[i], S) for i in range(len(R))))

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
    return phi[i] * J(R[i], Pinitial)


def simulate():
    S = int(p * N)
    Pinitial = [int((1.0 - p) * N)]
    P = [0] * M
    A = [0] * M
    R = [0] * M
    print('Initial Population:')
    print('S: {S}\nA: {A}\nR: {R}\nP: {P}'.format(S=S, A=A, R=R, P=P))
    while True:
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
        #1/0

if __name__ == '__main__':
    simulate()
