import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import MaxNLocator
import networkx as nx
from matplotlib.collections import LineCollection


__all__ = ['draw_stable_paths', 'plot_pareto', 'draw_multiples']


def draw_multiples(g, most_stable, pos=None):

    pos = pos or nx.kamada_kawai_layout(g)
    instability = np.array([v for _, v in most_stable.values()])

    points = [np.array([pos[u] for u in path])
              for path, _ in most_stable.values()]

    n = len(points)
    s = 3

    plt.figure(figsize=(s*n, s))
    colors = np.array(['lightgray', 'black'])

    for i, path in enumerate(points):
        background = LineCollection(points, linewidth=6, color='lightgray')
        lines = LineCollection([path], color='black')

        ax = plt.subplot(1, n, i + 1)
        ax.add_collection(background)
        ax.add_collection(lines)
        ax.scatter(*path[[0, -1]].T, s=100, c='k', zorder=2)
        ax.autoscale_view()

        plt.axis('equal')
        plt.xticks([])
        plt.yticks([])
        plt.title(f'{len(points[i])} / {instability[i]:.3f}')




def draw_stable_paths(g, most_stable, source, terminal, pos=None):
    plt.figure(figsize=(10,10))

    pos = pos or nx.drawing.kamada_kawai_layout(g)
    nx.draw(g, pos=pos, node_size=1, alpha=0.05)

    def draw_path(g, path, pos, linewidth=5):
        nodes = path
        edges = list(zip(path, path[1:]))

        nx.draw_networkx_nodes(g, nodelist=nodes, pos=pos, node_size=10)
        nx.draw_networkx_edges(g, edgelist=edges, pos=pos, linewidth=linewidth)

    for hops, (path, cost) in most_stable.items():
        draw_path(g, path, pos=pos)

    path, cost = most_stable[min(most_stable.keys())]
    draw_path(g, path, pos=pos, linewidth=200)

    nx.draw_networkx_nodes(g, nodelist=[source, terminal], pos=pos, node_color='g', node_size=55)

def plot_pareto(most_stable, all_stable_paths):
    # stabs = [p[1] for p in most_stable.values()]
    # lens = list(most_stable.keys())
        
    unoptimal_paths = np.array([(n, s[1]) for n, ps in all_stable_paths.items() for s in ps])
    optimal_paths = np.array([(n,ps[1]) for n, ps in most_stable.items()])

    ax = plt.figure(figsize=(20,10)).gca()  
    ax.xaxis.set_major_locator(MaxNLocator(integer=True)) 
    plt.subplot(111)

    cmap = plt.get_cmap('tab10')
    plt.scatter(unoptimal_paths[:,0], unoptimal_paths[:,1], color=cmap(1), label='Nonoptimal paths')
    plt.scatter(optimal_paths[:,0], optimal_paths[:,1], label='Optimal paths')
    plt.plot(optimal_paths[:,0], optimal_paths[:,1], label='Pareto frontier')


    plt.xlabel("Length of path")
    plt.ylabel("Instability of path")

    plt.legend()
    ticks = range(int(min(optimal_paths[:,0])), int(max(optimal_paths[:,0])) + 1)
    plt.xticks(ticks)
