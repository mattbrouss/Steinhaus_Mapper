import networkx as nx

__all__ = ['most_stable_paths']

def get_just_most_stable_for_each_length(all_stable_paths):
    most_stable = {}
    for hops, paths in all_stable_paths.items():
        most_stable[hops] = min(paths, key=lambda x: x[1])

    return most_stable

def most_stable_paths(g, source, terminal):
    """ Compute the pareto frontier of most stable paths
    
        Input: g the graph, source and terminal nodes as names of the nodes in g.
        Ouput: A dictionary with pairs {path length: (path, instability factor)}
    """
    all_stable_paths = jaccard_paths(g, source, terminal)
    most_stable = get_just_most_stable_for_each_length(all_stable_paths)
    return most_stable, all_stable_paths

def filter_edges(g, path_weights):
    e, s = max(path_weights, key=lambda x: x[1])
    
    edge_costs = nx.get_edge_attributes(g, 'dist')
    high_costs = [edge for edge, cost in edge_costs.items() if cost >= s]

    s,t = e
    assert e in high_costs or (t,s) in high_costs, f"Gotta remove the edge we want to remove, {e}:\n{high_costs}"
    g.remove_edges_from(high_costs)
    
def jaccard_paths(G, source, terminal):
    g = G.copy()
    paths = {}

    edge_map = nx.get_edge_attributes(g, 'dist')
    # import pdb    ; pdb.set_trace()
    while nx.has_path(g, source, terminal):
        shortest_path = list(nx.shortest_path(g, source, terminal))
        stab, path_weights = stability(edge_map, shortest_path)
        filter_edges(g, path_weights)
        
        hops = len(shortest_path)
            
        paths.setdefault(hops, []).append((shortest_path, stab))

    return paths

def stability(weight_map, path):
    """ weight_map is dictionary of edge to weights like `(s,t): weight`
        path will be specified as list of nodes
    """

    weights = []
    for s,t in zip(path, path[1:]):

        try:
            if (s,t) in weight_map.keys():
                weights.append(((s,t), weight_map[(s,t)]))
            else:
                weights.append(((s,t), weight_map[(t,s)]))
        except KeyError:
            print(f"Why is {(t,s)} or {(s,t)} not found in {weight_map}")
            raise

    # weights = [((s,t), weight_map[(s,t)] if (s,t) in weight_map else weight_map[(t,s)]) 
    #            for s,t in zip(path, path[1:])]
    s = max(e[1] for e in weights)
        
    return s, weights



