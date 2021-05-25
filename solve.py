import numpy as np
from scipy.optimize import minimize, Bounds, LinearConstraint
import scipy.integrate as integrate

def jac(x, G):
    n = G.graph["n"]
    res = []
    for i in range(n):
        for j in range(n):
            cost = G[i][j]["cost"]
            res.append(cost(x[i*n+j]))
    return res 

def cost(x, G):
    n = G.graph["n"]
    res = 0
    for i in range(n):
        for j in range(n):
            cost = G[i][j]["cost"]
            res += integrate.quad(cost, 0, x[i*n+j])[0]
    return res 

def solve(G, source):
    if np.sum(source) != 0:
        print("solve : source isn't balanced")

    n = G.graph["n"]
    x0 = np.full((n*n,), 0)
    bounds = Bounds(np.zeros((n*n,)), np.full((n*n,), np.infty))

    # constraint matrix for junctions
    A = np.zeros((n, n*n))
    for i in range(n):
        # i-th constraint
        for j in range(n):
            if G[i][j]["is_true"]:
                A[i, i*n + j] = 1
            if G[j][i]["is_true"]:
                A[i, j*n + i] = -1
    junc_constraint = LinearConstraint(A, np.array(source), np.array(source))

    result = minimize(cost, x0, args=(G,), bounds=bounds, \
        constraints=junc_constraint, \
        jac=jac, tol=1e-5, method='trust-constr')
    print("ended with message :", result.message)
    
    for i in range(n):
        for j in range(n):
            G[i][j]["flow"] = result.x[i*n + j]


