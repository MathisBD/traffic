import graph
from random import seed
from solve import solve 
import scipy.integrate as integrate
import numpy as np

seed(42)


def max_imbalance(G, source):
    n = G.graph["n"]
    res = 0
    for i in range(n):
        imb = source[i]
        for j in range(n):
            if G[j][i]["is_true"]:
                imb += G[j][i]["flow"]
            if G[i][j]["is_true"]:
                imb -= G[i][j]["flow"]
        res = max(res, abs(imb))
    return res

def max_neg_flow(G):
    res = 0
    for (x, y, d) in G.edges(data=True):
        if d["flow"] < 0:
            res = max(res, abs(d["flow"]))
    return res

def max_false_flow(G):
    res = 0
    for (x, y, d) in G.edges(data=True):
        if not d["is_true"]:
            res = max(res, abs(d["flow"]))
    return res

n = 8
G = graph.generate_graph(n, 20)
#graph.draw_graph(G)

source = [0 for _ in range(n)]
source[6] = 2
source[7] = 2
source[2] = -4
solve(G, source)

print("largest node imbalance = %f" % max_imbalance(G, source))
print("largest negative flow = %f" % max_neg_flow(G))
print("largest flow on false edge = %f" % max_false_flow(G))

graph.draw_graph(G)

