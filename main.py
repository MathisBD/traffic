from graph import show_graph, random_graph, intersect
from random import seed
from solve import solve 
import scipy.integrate as integrate
import numpy as np

seed(42)

g = random_graph(10, 100)
#show_graph(g)

source = [0 for _ in range(g.n)]
source[8] = 3
source[3] = -3
solve(g, source)

for i in range(g.n):
    bal = 0
    for j in range(g.n):
        bal += g.flow[i][j]
        bal -= g.flow[j][i]
    print("balance at %d=%f" % (i, bal))
print(np.sum(g.flow))

show_graph(g)

