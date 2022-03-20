import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_edgelist('facebook_combined.txt', create_using=nx.Graph(), nodetype=int)
pos1 = nx.spring_layout(G, seed=1)
### Reads the edgelist of SNAP data

plt.figure(1)
nx.draw(G, pos1, with_labels=False, node_size=10, node_color='#F1948A', edgecolors='#E74C3C')
plt.savefig('Facebook Ego Network Visualisation', bbox_inches='tight', dpi=300)
plt.show()
### Plots the SNAP data
