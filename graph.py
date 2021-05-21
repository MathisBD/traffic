
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
        return 1
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
            else:
                costs[i][j] = lambda flow: 0

    return Graph(n, positions, flow, capacities, costs)

def show_graph(g):
    max_flow = 0
    for i in range(g.n):
        for j in range(g.n):
            max_flow = max(g.flow[i][j], max_flow)
    
    for i in range(g.n):
        plt.text(g.positions[i][0], g.positions[i][1], "%d" % i)
    
    def draw_edge(i, j):
        if max_flow == 0:
            w = 0.5
        else:
            w = g.flow[i][j] / max_flow
        w *= 0.01

        a = g.positions[i]
        b = g.positions[j]
        plt.arrow(a[0], a[1], b[0] - a[0], b[1] - a[1], \
            width=w, head_width=max(3*w, 3*0.005), length_includes_head=True)
        plt.text((a[0] + b[0]) / 2.0, 0.01 + (a[1] + b[1]) / 2.0, \
            "%.2f/%.2f" % (g.flow[i][j], g.capacities[i][j]))

    for i in range(g.n):
        for j in range(g.n):
            if g.capacities[i][j] > 0:
                draw_edge(i, j)
    plt.show()
