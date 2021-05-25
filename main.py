import graph
from random import seed
from solve import solve 
import scipy.integrate as integrate
import numpy as np

seed(42)

n = 8
G = graph.generate_graph(n, 20)
#graph.draw_graph(G)

source = [0 for _ in range(n)]
source[6] = 3
source[2] = -3
solve(G, source)

graph.draw_graph(G)

