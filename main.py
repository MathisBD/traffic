from graph import show_graph, random_graph, intersect
from random import seed
from solve import solve 

seed(42)

g = random_graph(10, 17)
#show_graph(g)

source = [0 for _ in range(g.n)]
source[0] = 2
source[8] = -2
solve(g, source)

show_graph(g)
