#networkx is a library for working with graph data structures

import networkx as nx
import community
import matplotlib.pyplot as plt
from sklearn import metrics

dmat = metrics.pairwise_distances(quitmatrix, metric = 'cosine')
amat = dmat<0.6
G= nx.from_numpy_matrix(amat)

#community detection

part = community.best_partition(G)
mod = community.modularity(part, G)

#plot, color nodes using community structures

values = [part.get(node) for node in G.nodes()]
nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size = 30, with_labels = False)
plt.show()