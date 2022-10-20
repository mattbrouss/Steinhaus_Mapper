import numpy as np
import networkx as nx

def random_st(g, seed=12345):
    np.random.seed(seed)
    source, terminal = np.random.choice(g.nodes, 2)
    return source, terminal


def random_graph(nodes, density):

    edges = {}
    e1 = list(np.random.choice(nodes, int(nodes*nodes*density)))
    e2 = list(np.random.choice(nodes, int(nodes*nodes*density)))
    for i, j in zip(e1, e2):
        i,j = (i,j) if i <= j else (j, i)
        r = np.random.random()
        edges[(i,j)] = r

    g = nx.Graph()
    g.add_edges_from(edges)
    nx.set_edge_attributes(g, edges, 'dist')

    return g