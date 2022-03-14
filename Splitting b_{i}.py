import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpmath import *
import random
from operator import itemgetter

n = 40
q = 1/20
### Variables used to specify the ER network will have mean degree c = 2

G = nx.erdos_renyi_graph(n,q, seed=34, directed=False)
### Generates a new random ER2 Graph for N = 40

RemovedEdges = []
### List of the edges that are removed

for i in range(len(list(G.edges))):
    ### Repeats the process of solving the microscopic equations and removing the edge with the lowest bredge probability

    SliceList = []
    ### This is a list that all the values and correponding edges will be added to

    p = 0.9999
    ### States that nodes are kept in a single realisation of the percolation process with probability 0.9999

    gjiold = {}
    for i in list(G.nodes):
        for j in list(G.adj[i]):
            gjiold["g{0}old{1}".format(j,i)] = 1
    ### Sets initial condition for all gji in the network such that all gji equal one

    ###### To calculate new values if gji
    maxvalue = 1
    while maxvalue != 0:
        gjinew = {}
        maxlist = []
        ### This is a list of the absolute difference between the newly calculated gji and the inital condition
        for i in list(G.nodes):
            for j in list(G.adj[i]):
                ### Establishes the neighbourhood of j with i removed
                listforl = []
                for k in list(G.adj[j]):
                    if k != i:
                        listforl.append(k)
                    else:
                        pass
                ###### Uses the neighbourhood of j\i to calculate new values of gji
                if listforl == []:
                    gjinew["g{0}new{1}".format(j,i)] = 0
                    ### if j\i is empty it sets the new value of gji to be zero following our formula

                else:
                    ### Calculating the product of all (1-p*glj)
                    productlist = []
                    for l in list(listforl):
                        if 'g{0}new{1}'.format(l,j) in gjinew:
                            productlist.append(1-p*gjinew["g{0}new{1}".format(l,j)])
                            ### If a glj has already been calculated in this iteration it will be used instead of the initial condition
                        else:
                            productlist.append(1-p*gjiold["g{0}old{1}".format(l,j)])
                            ### If a glj has not already been calculated in this iteration it will be used the initial condition
                    x = 1
                    for z in list(productlist):
                        x = x * z
                    gjinew["g{0}new{1}".format(j,i)] = 1 - x
            
                maxlist.append(abs(gjinew["g{0}new{1}".format(j,i)]-gjiold["g{0}old{1}".format(j,i)]))
        maxvalue = round(max(maxlist), 2)
        ### This iterates until the values of gji don't change by more than three decimal places.  

        ###### Sets the gjiold to the newly calculated gjinew for the next iteration, giving a new initial condition
        gjiold = {}
        for i in list(G.nodes):
            for j in list(G.adj[i]):
                gjiold["g{0}old{1}".format(j,i)] = gjinew["g{0}new{1}".format(j,i)]

    ###### Calculates values of b_{ij} and adds them to a list
    bij = {}
    for i in list(G.nodes):
        for j in list(G.adj[i]):
            if i > j:
                ### Calculting the bredge probability
                bij["{0}b{1}".format(i,j)] = 1 - gjinew["g{0}new{1}".format(i,j)]*gjinew["g{0}new{1}".format(j,i)]
                SliceList.append((bij["{0}b{1}".format(i,j)],(j,i)))
            else:
                pass

    if min(SliceList, key=itemgetter(0))[0] < 0.85:
        G.remove_edge(*min(SliceList, key=itemgetter(0))[1])
        RemovedEdges.append(min(SliceList, key=itemgetter(0))[1])
        ### Searches the slicelist for the minimal bredge probability and removes its corresponding edge

print(RemovedEdges)
### Lists what edges were removed

SplitNodes = []
### A list of edges and their bredge probabilities that will be removed
for i in range(10):
    G.remove_edge(*max(SliceList, key=itemgetter(0))[1])
    SplitNodes.append(max(SliceList, key=itemgetter(0))[1])
    SliceList.remove(max(SliceList, key=itemgetter(0)))
### Removes the edge with the largest bredge probability

print(SplitNodes)
### Lists what edges were removed

plt.figure(1)
pos1 = nx.spring_layout(G, k=0.90, iterations=130, seed=20033)
nx.draw(G, pos1, with_labels=True, node_size=200, font_size=9, font_color='black', node_color='#FF8080')
nx.draw_networkx_nodes(G, pos1, nodelist=list(nx.articulation_points(G)), node_size=200, node_color='#6FED7C')
nx.draw_networkx_edges(G, pos1, edgelist=list(nx.bridges(G)), edge_color='#80c0ff')
plt.savefig('ER2 N=40 Seed=34 Split (b_{i})', bbox_inches='tight', dpi=300)
plt.show()
### Plots the dismantled graph
