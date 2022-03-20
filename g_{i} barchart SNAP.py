import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpmath import *
import random

n=10000
m=2

G = nx.read_edgelist('facebook_combined.txt', create_using=nx.Graph(), nodetype=int)
### Generates Facebook ego network

p = 0
plist = []
gibar = []
colour = ['#6699CC','#256cb4']

while p <= 1:

    plist.append(p)
    ### adds the value of p in the iteration to the list of values of p to use as the x axis


    ### Solve for g_{j}^{i}
    gjiold = {}
    for i in list(G.nodes):
        for j in list(G.adj[i]):
            gjiold["g{0}old{1}".format(j,i)] = 1
            ### Sets initial condition for all gji in the network such that all gji equal one

    ###### To calculate new values if gji###### To calculate new values if gji
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
                    ### Calculating the product of all (1-p*glj)### Calculating the product of all (1-p*glj)
                    productlist = []
                    for l in list(listforl):
                        if 'g{0}new{1}'.format(l,j) in gjinew:
                            productlist.append(1-p*gjinew["g{0}new{1}".format(l,j)])
                            ### If a glj has already been calculated in this iteration it will be used instead of the initial condition
                        else:
                            productlist.append(1-p*gjiold["g{0}old{1}".format(l,j)])
                            ### If a glj has not already been calculated in this iteration it will be used the initial conditioncondition
                    x = 1
                    for z in list(productlist):
                        x = x * z
                    gjinew["g{0}new{1}".format(j,i)] = 1 - x
            
                maxlist.append(abs(gjinew["g{0}new{1}".format(j,i)]-gjiold["g{0}old{1}".format(j,i)]))
        maxvalue = round(max(maxlist), 2)

        print("Iteration number", iteration, "for p =", p, ", Absolute difference =", maxvalue)
        iteration = iteration + 1
        ### This iterates until the values of gji don't change by more than three decimal places.

        #print("Iteration number", iteration, "for p =", p, ", Absolute difference =", maxvalue)
        gjiold = {}
        for i in list(G.nodes):
            for j in list(G.adj[i]):
                gjiold["g{0}old{1}".format(j,i)] = gjinew["g{0}new{1}".format(j,i)]

    ### Solve for g_{i} and averaging g_{i} for a single bar of the bar chart
    gi = {}
    giList = []
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
            giList.append(1 - x)
    ### averages over the number of nodes in the network
    y = 0
    for k in giList:
        y = y + k
    gibar.append(y/n)

    p = round(p+0.01, 2)

###### All plots

### Plots the betwork with articulation points and bredges highlighted
y_pos = np.arange(len(plist))
plt.figure(2)
plt.bar(y_pos, gibar, width = 1.0, align='center', color=colour, alpha=0.5)
plt.xticks([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
           [0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00], rotation = 90)
plt.xlabel('p')
plt.ylabel(r'$\bar{g}$')
plt.savefig('Facebook Average Barchart', bbox_inches='tight', dpi=300)
plt.show()
