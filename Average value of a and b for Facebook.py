import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpmath import *
import random
from numpy import asarray
from numpy import savetxt

G = nx.read_edgelist('facebook_combined.txt', create_using=nx.Graph(), nodetype=int)
### Generates Facebook ego network.

p = 1

plist = []
aiBar = []
bijBar = []
### Lists for the average values of a_{i} and b_{ij} for the facebook ego network

while p <= 1:

    plist.append(p)
    ### adds the value of p in the iteration to the list of values of p to use as the x axis

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
        maxvalue = round(max(maxlist), 3)
        ### This iterates until the values of gji don't change by more than three decimal places.

        gjiold = {}
        for i in list(G.nodes):
            for j in list(G.adj[i]):
                gjiold["g{0}old{1}".format(j,i)] = gjinew["g{0}new{1}".format(j,i)]

    ### Calculates values of b_{ij}
    bij = {}
    bijBarTemp = []
    for i in list(G.nodes):
        for j in list(G.adj[i]):
            if i > j:
                bij["{0}b{1}".format(i,j)] = 1 - gjinew["g{0}new{1}".format(i,j)]*gjinew["g{0}new{1}".format(j,i)]
                bijBarTemp.append(bij["{0}b{1}".format(i,j)])

    ### Calculates average value of b_{ij}
    x = 0
    y = len(list(bijBarTemp))
    for i in bijBarTemp:
        x = x + i
    bijBar.append(x/y)

    ### Calculates values of a_{i}
    ai = {}
    aiBarTemp = []
    for i in list(G.nodes):
        sumlist = []
        productlist = []
        for j in list(G.adj[i]):
            sumlist.append(1 - gjinew["g{0}new{1}".format(j,i)])
            productlist.append(1 - p + p*gjinew["g{0}new{1}".format(j,i)])
        x = 0
        for y in sumlist:
            x = x + y
        z = 1
        for y in productlist:
            z = z * y
        if G.degree[i] >= 2:
            ai["a{0}".format(i)] = 1-p*((1-p)**(G.degree[i]-1))*x-z
            aiBarTemp.append(ai["a{0}".format(i)])
        else:
            ai["a{0}".format(i)] = 0
            aiBarTemp.append(ai["a{0}".format(i)])

    ### Calculates average value of a_{i}
    x = 0
    y = len(list(aiBarTemp))
    for i in aiBarTemp:
        x = x + i
    aiBar.append(x/y)

    print(p)

    p = round(p + 0.01, 2)

Averageai = asarray(aiBar)
savetxt('Averageai.csv', Averageai, delimiter=',')
### Saves data used in the plot

Averagebij = asarray(bijBar)
savetxt('Averagebij.csv', Averagebij, delimiter=',')
### Saves data used in the plot
