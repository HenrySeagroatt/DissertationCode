import networkx as nx
import matplotlib.pyplot as plt
import random

n=40
q=(1/20)
#Specifies the initial conditions used to generate an Erdös-Rényi network with mean degree c=2 and N=40 nodes

### Full Network
G = nx.erdos_renyi_graph(n,q,seed=34, directed=False) #Generates the Erdös-Rényi network used in Figure 1 that we will manipulate throughout
pos1 = nx.spring_layout(G, k=0.74, iterations=104, seed=20033) #Provides a replicable layout so that the network is easily readable

plt.figure(1)
nx.draw(G, pos1, with_labels=True, node_size=200, font_size=9, font_color='black', node_color='#FF8080')
plt.savefig('ER2 N=40 Seed=34 Figure1', bbox_inches='tight', dpi=300) #Saves the image generated

### Network with articulation points highlighted
G = nx.erdos_renyi_graph(n,q,seed=34, directed=False)
pos1 = nx.spring_layout(G, k=0.74, iterations=104, seed=20033) #Provides a replicable layout so that the network is easily readable

plt.figure(2)
nx.draw(G, pos1, with_labels=True, node_size=200, font_size=9, font_color='black', node_color='#FF8080')
nx.draw_networkx_nodes(G, pos1, nodelist=list(nx.articulation_points(G)), node_size=200, node_color='#6FED7C') #Colours the articulation points green
plt.savefig('ER2 N=40 Seed=34 Figure2', bbox_inches='tight', dpi=300) #Saves the image generated

### Network with bredges highlighted
G = nx.erdos_renyi_graph(n,q,seed=34, directed=False)
pos1 = nx.spring_layout(G, k=0.74, iterations=104, seed=20033) #Provides a replicable layout so that the network is easily readable

plt.figure(3)
nx.draw(G, pos1, with_labels=True, node_size=200, font_size=9, font_color='black', node_color='#FF8080')
nx.draw_networkx_edges(G, pos1, edgelist=list(nx.bridges(G)), edge_color='#80c0ff') #Colours the bredges blue
plt.savefig('ER2 N=40 Seed=34 Figure3', bbox_inches='tight', dpi=300) #Saves the image generated

### Network with all hightlighted
G = nx.erdos_renyi_graph(n,q,seed=34, directed=False)
pos1 = nx.spring_layout(G, k=0.74, iterations=104, seed=20033) #Provides a replicable layout so that the network is easily readable

plt.figure(4)
nx.draw(G, pos1, with_labels=True, node_size=200, font_size=9, font_color='black', node_color='#FF8080')
nx.draw_networkx_nodes(G, pos1, nodelist=list(nx.articulation_points(G)), node_size=200, node_color='#6FED7C') #Colours the articulation points green
nx.draw_networkx_edges(G, pos1, edgelist=list(nx.bridges(G)), edge_color='#80c0ff') #Colours the bredges blue
plt.savefig('ER2 N=40 Seed=34 Figure4', bbox_inches='tight', dpi=300) #Saves the image generated

### Network with all articulation points removed
G = nx.erdos_renyi_graph(n,q,seed=34, directed=False)
pos1 = nx.spring_layout(G, k=0.74, iterations=104, seed=20033) #Provides a replicable layout so that the network is easily readable

plt.figure(5)
G.remove_nodes_from(list(nx.articulation_points(G))) #Removes all articulation points from the network
nx.draw(G, pos1, with_labels=True, node_size=200, font_size=9, font_color='black', node_color='#FF8080')
plt.savefig('ER2 N=40 Seed=34 Figure5', bbox_inches='tight', dpi=300) #Saves the image generated

### Network with all bredges removed
G = nx.erdos_renyi_graph(n,q,seed=34, directed=False)
pos1 = nx.spring_layout(G, k=0.74, iterations=104, seed=20033)

plt.figure(6)
G.remove_edges_from(list(nx.bridges(G))) #Removes all bredges from the network
nx.draw(G, pos1, with_labels=True, node_size=200, font_size=9, font_color='black', node_color='#FF8080')
plt.savefig('ER2 N=40 Seed=34 Figure6', bbox_inches='tight', dpi=300) #Saves the image generated

plt.show()
