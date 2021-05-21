
from collections import namedtuple
from typing import NamedTuple
from random import random, shuffle
from collections.abc import Callable
import matplotlib.pyplot as plt
from linesegmentintersections import bentley_ottman


class Graph:
    def __init__(self, n, positions, flow, capacities, costs):
        self.n = n
        self.positions = positions 
        self.flow = flow
        self.capacities = capacities 
        self.costs = costs

def build_trivial_cost(capacity):
    def cost(flow):
        return flow / float(capacity)
    return cost


def intersect(line1, line2):
    if bentley_ottman([line1, line2]):
        return True 
    else:
        return False     

def can_add_edge(capacities, positions, a, b): 
    if a == b:
        return False 
    if capacities[a][b] > 0 or capacities[b][a] > 0:
        return False

    n = len(positions)
    for i in range(n):
        for j in range(n):
            if capacities[i][j] == 0:
                continue
            if a == i or a == j or b == i or b == j:
                continue 
            if intersect([positions[a], positions[b]], [positions[i], positions[j]]):  
                return False 
    return True 

# will try to put as many as max_edge_num edges, 
# but can put less if it doesn't manage to.
def random_graph(n, max_edge_num):
    # positions
    positions = [] 
    for i in range(n):
        positions.append([random(), random()])
    
    # capacities 
    edges = []
    for i in range(n):
        for j in range(n):
            edges.append((i, j))
    shuffle(edges)

    capacities = [[0 for _ in range(n)] for _ in range(n)]
    count = 0
    for (i, j) in edges:
        if count >= max_edge_num:
            break 
        if can_add_edge(capacities, positions, i, j):
            capacities[i][j] = 10*random()
            count += 1
        else:
            capacities[i][j] = 0

    # flow
    flow = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            flow[i][j] = 0

    # costs
    costs = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if capacities[i][j] > 0:
                costs[i][j] = build_trivial_cost(capacities[i][j])
    
    return Graph(n, positions, flow, capacities, costs)

def show_graph(g):
    plt.plot(*list(zip(*g.positions)), 'ro')
    for i in range(g.n):
        for j in range(g.n):
            if g.capacities[i][j] > 0:
                xx = [g.positions[i][0], g.positions[j][0]]
                yy = [g.positions[i][1], g.positions[j][1]]
                plt.plot(xx, yy, 'b')
                plt.text((xx[0] + xx[1]) / 2.0, 0.01 + (yy[0] + yy[1]) / 2.0, \
                    "%.1f/%.1f" % (g.flow[i][j], g.capacities[i][j]))
    plt.show()
