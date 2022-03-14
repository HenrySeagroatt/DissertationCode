import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpmath import *
import random

n=40
q = 1/20
### Variables used to specify the ER network will have mean degree c = 2

G = nx.erdos_renyi_graph(n,q,seed=34, directed=False)
### Generates a new random ER2 Graph for N = 40

#G=nx.Graph()
#G.add_nodes_from([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
#G.add_edges_from([(23,25),(24,25),(25,26),(27,28),(28,29),(1,3),(2,3),(3,4),(4,5),(5,6),(7,6),(8,6),(9,6),(6,10),(11,10),(18,19),(19,20),(22,21),(21,16),(16,14),(16,17),(17,13),(17,15),(14,18),(14,12),(12,10),(12,15),(10,13),(13,15),(13,18),(15,18)])
#print(list(nx.bridges(G)))

p = 0
ArrayForA = []
### A list of lists of artulation point probabilities for each p
ArrayForB = []
### A list of lists of bredge probabilities for each p
plist = []
### A list of values of p to use as the x axis

while p <= 1:

    gjiold = {}
    for i in list(G.nodes):
        for j in list(G.adj[i]):
            gjiold["g{0}old{1}".format(j,i)] = 1
            ### Sets initial condition for all gji in the network such that all gji equal one

    plist.append(p)
    ### adds the value of p in the iteration to the list of values of p to use as the x axis

    ###### To calculate new values if gji
    maxvalue = 1
    iteration = 1
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
        maxvalue = round(max(maxlist), 3)
        ### This iterates until the values of gji don't change by more than three decimal places.

        #print("Iteration number", iteration, "for p =", p, ", Absolute difference =", maxvalue)
        iteration = iteration + 1

        gjiold = {}
        for i in list(G.nodes):
            for j in list(G.adj[i]):
                gjiold["g{0}old{1}".format(j,i)] = gjinew["g{0}new{1}".format(j,i)]

    ### Calculates values of b_{ij} and puts them in an array so they can be plotted.
    ArrayColumnListForB = []
    bij = {}
    for i in list(G.nodes):
        for j in list(G.adj[i]):
            if i > j:
                ### Calculting the bredge probability
                bij["{0}b{1}".format(i,j)] = 1 - gjinew["g{0}new{1}".format(i,j)]*gjinew["g{0}new{1}".format(j,i)]
                #ArrayColumnListForB.append(1 - gjinew["g{0}new{1}".format(i,j)]*gjinew["g{0}new{1}".format(j,i)])
                ArrayColumnListForB.append(bij["{0}b{1}".format(i,j)])
            else:
                pass
    ArrayForB.append(ArrayColumnListForB)

    ### Calculates values of a_{i} and puts them in an array so they can be plotted.
    ArrayColumnListForA = []
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
        else:
            ai["a{0}".format(i)] = 0
        ### If ai = 1 (i.e is an articulation point) we will add it to a list of calculated articulation points

        ArrayColumnListForA.append(ai["a{0}".format(i)])
    ArrayForA.append(ArrayColumnListForA)

    p = round(p+0.01, 2)

###### All plots

### Plots the betwork with articulation points and bredges highlighted

### Plot for b_{ij}
plt.figure(1)
for j in range(len(ArrayColumnListForB)):
    templist=[]
    for i in range(len(ArrayForB)):
        templist.append(ArrayForB[i][j])
    plt.plot(plist,templist,'red')
plt.xlabel('p')
plt.ylabel(r'$b_{ij}$')
plt.grid()
plt.savefig('ER2 N=40 Seed=5 Bredges', bbox_inches='tight', dpi=300)

### Plot for a_{i}
plt.figure(2)
for j in range(len(ArrayColumnListForA)):
    templist=[]
    for i in range(len(ArrayForA)):
        templist.append(ArrayForA[i][j])
    plt.plot(plist,templist,'red')
plt.xlabel('p')
plt.ylabel(r'$a_{i}$')
plt.grid()
plt.savefig('ER2 N=40 Seed=5 Articulation Points', bbox_inches='tight', dpi=300)

### Plot for both
plt.figure(3)
for j in range(len(ArrayColumnListForB)):
    templist=[]
    for i in range(len(ArrayForB)):
        templist.append(ArrayForB[i][j])
    plt.plot(plist,templist,'blue')
for j in range(len(ArrayColumnListForA)):
    templist=[]
    for i in range(len(ArrayForA)):
        templist.append(ArrayForA[i][j])
    plt.plot(plist,templist,'red')
plt.xlabel('p')
plt.ylabel(r'$a_{i},b_{ij}$')
plt.grid()
plt.savefig('ER2 N=40 Seed=5 Articulation Points and Bredges', bbox_inches='tight', dpi=300)
plt.show()


