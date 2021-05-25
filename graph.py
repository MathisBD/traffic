import pygraphviz as pgv
import networkx as nx
import numpy as np
from random import random, shuffle
from linesegmentintersections import bentley_ottman


MIN_DIST = 0.1
COST_EPSILON = 1e-3


def dist(a, b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def can_add_pos(p, positions):
    for p2 in positions:
        if dist(p, p2) < MIN_DIST:
            return False 
    return True

def intersect(line1, line2):
    if bentley_ottman([line1, line2]):
        return True 
    else:
        return False     

def can_add_edge(x, y, true_edges, positions):
    if x == y:
        return False 
    if (x, y) in true_edges:
        return False
    for (a, b) in true_edges:
        if a == x or a == y or b == x or b == y:
            continue
        if intersect((positions[x], positions[y]), (positions[a], positions[b])):
            return False
    return True 

def generate_graph(n, max_edges):
    G = nx.DiGraph()
    G.graph['n'] = n
    # nodes 
    positions = []
    for i in range(n):
        tries = 0
        while tries < 100:
            p = (random(), random())
            if can_add_pos(p, positions):
                positions.append(p)
                G.add_node(i, pos=p)
                break 
        if tries >= 100:
            print("ERROR [generate_graph] : can't find a valid node position")
                
    # edges
    edges = [(i,j) for i in range(n) for j in range(n)]
    shuffle(edges)
    # costs
    count = 0
    true_edges = []
    for (x, y) in edges:
        if count < max_edges and can_add_edge(x, y, true_edges, positions):
            G.add_edge(x, y, 
                cost=lambda f: f,
                cost_deriv=lambda f: 1, 
                flow=0,
                is_true=True)
            true_edges.append((x,y))
            count += 1
        else:
            G.add_edge(x, y, 
                cost=lambda f: f / COST_EPSILON,
                cost_deriv=lambda f: 1 / COST_EPSILON,
                flow=0,
                is_true=False)
    return G

def draw_graph(G):
    gv = pgv.AGraph(strict=False, directed=True)
    
    # nodes
    for (x, d) in G.nodes(data=True):
        p = d["pos"]
        gv.add_node(x, 
            pos=("%.2f, %.2f" % (p[0]*10, p[1]*10)),
            pin="true",
            color="goldenrod1", 
            style="filled", 
            fillcolor="goldenrod1")
    
    # get max flow value
    max_flow = 0
    for (x,y,d) in G.edges(data=True):
        max_flow = max(max_flow, d['flow'])
    
    # edges
    for (x,y,d) in G.edges(data=True):
        if d['is_true']:
            # compute alpha value (range 0-255)
            if max_flow <= 1e-2:
                alpha = 255
            else:
                alpha = 255 * (np.sqrt(d['flow'] / float(max_flow)))
            alpha = min(max(int(alpha), 0), 255)

            gv.add_edge(x,y,
                label=("%.2f" % d['flow']), 
                color=("#0000CC%2x" % alpha), 
                penwidth=3)

    gv.node_attr['color'] = 'red'
    gv.write("graph.dot")
    gv.draw("graph.png", prog="neato")


