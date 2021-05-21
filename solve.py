import numpy as np
from scipy.optimize import minimize, Bounds, LinearConstraint
import scipy.integrate as integrate

def jac(x, g):
    res = []
    for i in range(g.n):
        for j in range(g.n):
            c = g.costs[i][j]
            res.append(c(x[i*g.n + j]))
    return res 

def cost(x, g):
    res = 0
    for i in range(g.n):
        for j in range(g.n):
            res += integrate.quad(g.costs[i][j], 0, x[i*g.n + j])[0]
    return res 

def solve(g, source):
    if np.sum(source) != 0:
        print("solve : source isn't balanced")

    n = g.n
    x0 = np.full((n*n,), 0.0)
    bounds = Bounds(np.zeros((n*n,)), np.array(g.capacities).flatten(), keep_feasible=True)

    # constraint matrix for junctions
    A = np.zeros((n, n*n))
    for i in range(n):
        # i-th constraint
        for j in range(n):
            if g.capacities[i][j] > 0:
                A[i, i*g.n + j] = 1
            if g.capacities[j][i] > 0:
                A[i, j*g.n + i] = -1
    junc_constraint = LinearConstraint(A, np.array(source), np.array(source))

    result = minimize(cost, x0, args=(g,), bounds=bounds, \
        constraints=junc_constraint, tol=1e-3, method='trust-constr')
    print("ended with message :", result.message)
    
    for i in range(g.n):
        for j in range(g.n):
            g.flow[i][j] = result.x[i*g.n + j]


