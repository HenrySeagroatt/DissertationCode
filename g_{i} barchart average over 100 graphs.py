import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpmath import *
import random
from operator import itemgetter

n = 5000
q = 1/2500
### Variables used to specify the ER network will have mean degree c = 2

k2 = nsum(lambda k:(k**2)*((((n*q)**k)*((mp.e)**(-(n*q))))/fac(k)), [0,inf])
k1 = nsum(lambda k:(k)*((((n*q)**k)*((mp.e)**(-(n*q))))/fac(k)), [0,inf])
critical = (k2-k1)/k1
### Used in the calculation of the percolation threshold

colour = ['#6699CC','#256cb4']

giBarTotal = []
giBarAverage = []

for counter in range(100):
    G = nx.erdos_renyi_graph(n,q, seed=counter, directed=False)

    p = 0
    gibar = []
    while p <= 1:
        
        gjiold = {}
        for i in list(G.nodes):
            for j in list(G.adj[i]):
                gjiold["g{0}old{1}".format(j,i)] = 1
                ### Sets initial condition for all gji in the network such that all gji equal one

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
            maxvalue = round(max(maxlist), 2)
            ### This iterates until the values of gji don't change by more than three decimal places.


            #print("Iteration number", iteration, "for p =", p, ", Absolute difference =", maxvalue)
            iteration = iteration + 1

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
    print("Number of graphs analysed...", counter)
    giBarTotal.append(gibar)

for j in range(len(gibar)):
    Tally = 0
    for i in range(100):
        Tally = Tally + giBarTotal[i][j]
    giBarAverage.append(Tally/100)
    ###Averages each bar corresponding to the same p value for each of the 100 graphs

plist = []
zlist = []
p = 0
while p <= 1:

    plist.append(p)
    
    ### A copy of the macroscopic curve
    mp.dps = 3
    x = 0.95 ### Any initial condition, just needs to be different from 0 (the trivial solution)
    z = 0.1 ### (arbitrary, good as long as its not the same as x)
    if p == 1/(n*q):
        while z != x:
            x = round(nsum(lambda k:(k/(n*q))*((((n*q)**k)*(mp.e**(-(n*q))))/fac(k))*(1-(1-(p*x))**(k-1)),[1,inf]),6)
            z = round(nsum(lambda k:(k/(n*q))*((((n*q)**k)*(mp.e**(-(n*q))))/fac(k))*(1-(1-(p*x))**(k-1)),[1,inf]),6)
        zlist.append(nsum(lambda k:((((n*q)**k)*(mp.e**(-(n*q))))/fac(k))*(1-(1-(p*z))**(k)),[0,inf]))
    else:
        while z!= x:
            x = nsum(lambda k:(k/(n*q))*((((n*q)**k)*(mp.e**(-(n*q))))/fac(k))*(1-(1-(p*x))**(k-1)),[1,inf])
            z = nsum(lambda k:(k/(n*q))*((((n*q)**k)*(mp.e**(-(n*q))))/fac(k))*(1-(1-(p*x))**(k-1)),[1,inf])
        zlist.append(nsum(lambda k:((((n*q)**k)*(mp.e**(-(n*q))))/fac(k))*(1-(1-(p*z))**(k)),[0,inf]))
        ### Cobwevs for each value of p
    if p*critical == 1:
        pc = p
        print("Critical probability", pc)
    else:
        pass
    ### Identifies the critical point

    p = round(p+0.01, 2)

###### All plots
y_pos = np.arange(len(plist))
plt.figure(1)
plt.bar(y_pos, giBarAverage, width = 1.0, align='center', color=colour, alpha=0.5)
plt.plot(y_pos, zlist, 'black')
plt.plot(50, 0, marker=".", markersize=10, markeredgecolor='#FF8080', markerfacecolor='#FF8080')
plt.xticks([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
           [0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00], rotation = 90)
plt.xlabel('p')
plt.ylabel(r'$\bar{g}$')
plt.savefig('Average ER2 N=5000', bbox_inches='tight', dpi=300)
plt.show()
