import pygraphviz as pgv
import networkx as nx
import numpy as np


def draw_graph(G):
    gv = pgv.AGraph(strict=False, directed=True)
    
    # nodes
    for x in G.nodes():
        gv.add_node(x, 
            color="goldenrod1", 
            style="filled", 
            fillcolor="goldenrod1")
    
    # get max flow value
    max_flow = 0
    for (x,y,d) in G.edges(data=True):
        max_flow = max(max_flow, d['flow'])
    
    # edges
    for (x,y,d) in G.edges(data=True):
        # compute alpha value (range 0-255)
        if max_flow <= 1e-2:
            alpha = 255
        else:
            alpha = 255 * (np.sqrt(d['flow'] / float(max_flow)))
        alpha = min(max(int(alpha), 0), 255)

        gv.add_edge(x,y,
            label=d['flow'], 
            color=("#0000CC%2x" % alpha), 
            penwidth=3)

    gv.node_attr['color'] = 'red'

    gv.draw("graph.png", prog="dot")


draw(G)

