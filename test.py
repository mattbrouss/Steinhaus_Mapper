import pytest
import networkx as nx
import numpy as np


from paths import paths
from paths import utils

def test_stability():
    g = utils.random_graph(20, 0.2)
    s, t = utils.random_st(g)
    shortest_path = nx.shortest_path(g, s, t)
    edge_map = nx.get_edge_attributes(g, 'dist')
    stab, path_weights = paths.stability(edge_map, shortest_path)