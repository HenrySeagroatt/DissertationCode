import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpmath import *
import time
from numpy import asarray
from numpy import savetxt

NumberOfNodes = []
for i in range(1,51):
    NumberOfNodes.append(i*100)
### Creates a list of numbers with difference of 100

TimeList = []
### Creates a list we will add the times it takes to calculate the macroscopic equations 

Counter = 1

for Number in NumberOfNodes:

    AverageList = []

    for Average in range(250):
        ### A loop which will generate an ER network with N nodes 250 times

        G = nx.erdos_renyi_graph(Number,(2/Number), directed=False)
        ### Generates a new Erdos Renyi network with mean degree c=2

        start = time.perf_counter()
        ### Value of p used in the percolation process

        p = 1

        ### Solve for g_{j}^{i}
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

        end = time.perf_counter()
        ### Notes what time the calculations end at
        AverageList.append(end-start)
        ### Adds the time it takes to solve each network with N nodes to a list

    AverageItem = 0
    for i in AverageList:
        AverageItem = AverageItem + i
    TimeList.append(AverageItem/100)
    ### Averages the time it takes to solve each network with the same number of nodes and adds it to a list to be used in the plot
    
    print('Loading...', Counter,'%', 'Number of Nodes', Number)
    ### A way of visualising how much of the code has completed
    Counter = Counter + 1

AverageTime = asarray(TimeList)
savetxt('AverageTime.csv', AverageTime, delimiter=',')
### Saves the list of times to a spreadsheet so we can plot it later
