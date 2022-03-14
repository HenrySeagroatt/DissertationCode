import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpmath import *
import random
from operator import itemgetter

n=40
q = 1/20
### Variables used to specify the ER network will have mean degree c = 2

G = nx.erdos_renyi_graph(n,q,seed=34, directed=False)
### Generates a new random ER2 Graph for N = 40

RemovedNodes = []
### List of the nodes that are removed

for i in range(n):
    ### Repeats the process of solving the microscopic equations and removing the node with the lowest articulation point probability

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
        maxvalue = round(max(maxlist), 3)
        ### This iterates until the values of gji don't change by more than three decimal places.  

        gjiold = {}
        for i in list(G.nodes):
            for j in list(G.adj[i]):
                gjiold["g{0}old{1}".format(j,i)] = gjinew["g{0}new{1}".format(j,i)]

    ### Calculates values of a_{i} and adds them to a list
    ai = {}
    for i in list(G.nodes):
        sumlist = []
        productlist = []
        for j in list(G.adj[i]):
            ### Calculates the sum component in the expression
            sumlist.append(1 - gjinew["g{0}new{1}".format(j,i)])
            ### Calculates the product component in the expression
            productlist.append(1 - p + p*gjinew["g{0}new{1}".format(j,i)])
        x = 0
        for y in sumlist:
            x = x + y
        z = 1
        for y in productlist:
            z = z * y
        ### We need to implement an indicator function for the degree of the node (i.e a point with degree 0 or 1 cant be an articulation point)
        if G.degree[i] >= 2:
            ai["a{0}".format(i)] = 1-p*((1-p)**(G.degree[i]-1))*x-z
            SliceList.append((ai["a{0}".format(i)], i))
        else:
            ai["a{0}".format(i)] = 0
            ### If ai = 1 (i.e is an articulation point) we will add it to a list of calculated articulation points

    if min(SliceList, key=itemgetter(0))[0] < 0.85:
        G.remove_node(min(SliceList, key=itemgetter(0))[1])
        RemovedNodes.append(min(SliceList, key=itemgetter(0))[1])
        ### Searches the slicelist for the minimal articulation point probability and removes its corresponding node


print(RemovedNodes)
### Lists what edges were removed

plt.figure(1)
pos1 = nx.spring_layout(G, k=0.74, iterations=104, seed=20033)
nx.draw(G, pos1, with_labels=True, node_size=200, font_size=9, font_color='black', node_color='#FF8080')
nx.draw_networkx_nodes(G, pos1, nodelist=list(nx.articulation_points(G)), node_size=200, node_color='#6FED7C')
nx.draw_networkx_edges(G, pos1, edgelist=list(nx.bridges(G)), edge_color='#80c0ff')
plt.savefig('ER2 N=40 Seed=34 Decycled (a_{i})', bbox_inches='tight', dpi=300)
plt.show()
### Plots the decycled graph
