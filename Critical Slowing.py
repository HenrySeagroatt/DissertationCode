import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpmath import *
import random

n = 40
q = 1/20

G = nx.erdos_renyi_graph(n,q, seed=34, directed=False)

p = 0
plist = []
IterationList = []
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

    IterationList.append(iteration)

    ### Solve for g_{i}
    gi = {}
    for i in list(G.nodes):
        if list(G.adj[i]) == []:
            gi["g{0}".format(i)] = 0
        else:
            productlist = []
            for j in list(G.adj[i]):
                productlist.append(1 - p*gjinew["g{0}new{1}".format(j,i)])
            x = 1
            for z in list(productlist):
                x = x * z
            gi["g{0}".format(i)] = 1 - x

    p = round(p+0.001, 3)

###### All plots

### Plots the betwork with articulation points and bredges highlighted
y_pos = np.arange(len(plist))
plt.figure(2)
plt.plot(y_pos, IterationList, 'black')
plt.xticks([0,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000],
           [0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00], rotation = 90)
plt.xlabel('p')
plt.ylabel('Number of Iterations to solve the microscopic equations')
plt.grid()
plt.savefig('ER2 N=40 Seed=34 Number of Iterations', bbox_inches='tight', dpi=300)
plt.show()
