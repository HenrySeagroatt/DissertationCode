import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpmath import *
import random

n=10000
m = 2

AverageNNumber = 100

AverageaiBarAll = []
AverageaiBar2 = []
AverageaiBar3 = []
AverageaiBar4 = []
AverageaiBar5Up = []

AveragebijBarAll = []
AveragebijBar2 = []
AveragebijBar3 = []
AveragebijBar4 = []
AveragebijBar5Up = []

AverageaiBarAllFinal = []
AverageaiBar2Final = []
AverageaiBar3Final = []
AverageaiBar4Final = []
AverageaiBar5UpFinal = []

AveragebijBarAllFinal = []
AveragebijBar2Final = []
AveragebijBar3Final = []
AveragebijBar4Final = []
AveragebijBar5UpFinal = []

for Counter in range(AverageNNumber):

    G = nx.barabasi_albert_graph(n,m)
    ### Generates a Barabasi-Alvert network with m=2

    p = 0.4

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
        ### This is a list of the absolute difference between the newly calculated gji and the inital 
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
    bijTupleList = []
    for i in list(G.nodes):
        for j in list(G.adj[i]):
            if i > j:
                ### Calculting the bredge probability
                bij["{0}b{1}".format(i,j)] = 1 - gjinew["g{0}new{1}".format(i,j)]*gjinew["g{0}new{1}".format(j,i)]
                bijTupleList.append((i,j,bij["{0}b{1}".format(i,j)],G.degree[i],G.degree[j]))

    ### Calculates values of a_{i}
    ai = {}
    aiTupleList = []
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

        aiTupleList.append((i, ai["a{0}".format(i)], G.degree[i]))
        

    a = 0
    alist = []

    aiBarAll = []
    aiBar2 = []
    aiBar3 = []
    aiBar4 = []
    aiBar5Up = []

    bijBarAll = []
    bijBar2 = []
    bijBar3 = []
    bijBar4 = []
    bijBar5Up = []

    while a <= 1:

        alist.append(a)

        ainumberAll = 0
        ainumber2 = 0
        ainumber3 = 0
        ainumber4 = 0
        ainumber5Up = 0

        bijnumberAll = 0
        bijnumber2 = 0
        bijnumber3 = 0
        bijnumber4 = 0
        bijnumber5Up = 0

        for i in range(len(list(aiTupleList))):
            if a == 0:
                if a <= aiTupleList[i][1] <= a + 0.01:
                    ainumberAll = ainumberAll + 1
                    if aiTupleList[i][2] == 2:
                        ainumber2 = ainumber2 + 1
                    if aiTupleList[i][2] == 3:
                        ainumber3 = ainumber3 + 1
                    if aiTupleList[i][2] == 4:
                        ainumber4 = ainumber4 + 1
                    if aiTupleList[i][2] >= 5:
                        ainumber5Up = ainumber5Up +1
            if 0.01 <= a < 0.98:
                if a < aiTupleList[i][1] <= a + 0.01:
                    ainumberAll = ainumberAll + 1
                    if aiTupleList[i][2] == 2:
                        ainumber2 = ainumber2 + 1
                    if aiTupleList[i][2] == 3:
                        ainumber3 = ainumber3 + 1
                    if aiTupleList[i][2] == 4:
                        ainumber4 = ainumber4 + 1
                    if aiTupleList[i][2] >= 5:
                        ainumber5Up = ainumber5Up +1
            if a == 0.99:
                if a < aiTupleList[i][1] < a + 0.01:
                    ainumberAll = ainumberAll + 1
                    if aiTupleList[i][2] == 2:
                        ainumber2 = ainumber2 + 1
                    if aiTupleList[i][2] == 3:
                        ainumber3 = ainumber3 + 1
                    if aiTupleList[i][2] == 4:
                        ainumber4 = ainumber4 + 1
                    if aiTupleList[i][2] >= 5:
                        ainumber5Up = ainumber5Up +1
            if a == 1:
                if a <= aiTupleList[i][1] <= a:
                    ainumberAll = ainumberAll + 1
                    if aiTupleList[i][2] == 2:
                        ainumber2 = ainumber2 + 1
                    if aiTupleList[i][2] == 3:
                        ainumber3 = ainumber3 + 1
                    if aiTupleList[i][2] == 4:
                        ainumber4 = ainumber4 + 1
                    if aiTupleList[i][2] >= 5:
                        ainumber5Up = ainumber5Up +1

        for i in range(len(list(bijTupleList))):
            if a == 0:
                if a <= bijTupleList[i][2] <= a + 0.01:
                    bijnumberAll = bijnumberAll + 1
                    if bijTupleList[i][3] == 2:
                        bijnumber2 = bijnumber2 + 1
                    if bijTupleList[i][3] == 3:
                        bijnumber3 = bijnumber3 + 1
                    if bijTupleList[i][3] == 4:
                        bijnumber4 = bijnumber4 + 1
                    if bijTupleList[i][3] >= 5:
                        bijnumber5Up = bijnumber5Up + 1
            if 0.01 <= a < 0.98:
                if a < bijTupleList[i][2] <= a + 0.01:
                    bijnumberAll = bijnumberAll + 1
                    if bijTupleList[i][3] == 2:
                        bijnumber2 = bijnumber2 + 1
                    if bijTupleList[i][3] == 3:
                        bijnumber3 = bijnumber3 + 1
                    if bijTupleList[i][3] == 4:
                        bijnumber4 = bijnumber4 + 1
                    if bijTupleList[i][3] >= 5:
                        bijnumber5Up = bijnumber5Up + 1
            if a == 0.99:
                if a < bijTupleList[i][2] < a + 0.01:
                    bijnumberAll = bijnumberAll + 1
                    if bijTupleList[i][3] == 2:
                        bijnumber2 = bijnumber2 + 1
                    if bijTupleList[i][3] == 3:
                        bijnumber3 = bijnumber3 + 1
                    if bijTupleList[i][3] == 4:
                        bijnumber4 = bijnumber4 + 1
                    if bijTupleList[i][3] >= 5:
                        bijnumber5Up = bijnumber5Up + 1
            if a == 1:
                if a <= bijTupleList[i][2] <= a:
                    bijnumberAll = bijnumberAll + 1
                    if bijTupleList[i][3] == 2:
                        bijnumber2 = bijnumber2 + 1
                    if bijTupleList[i][3] == 3:
                        bijnumber3 = bijnumber3 + 1
                    if bijTupleList[i][3] == 4:
                        bijnumber4 = bijnumber4 + 1
                    if bijTupleList[i][3] >= 5:
                        bijnumber5Up = bijnumber5Up + 1


        aiBarAll.append(ainumberAll/100)
        aiBar2.append(ainumber2/100)
        aiBar3.append(ainumber3/100)
        aiBar4.append(ainumber4/100)
        aiBar5Up.append(ainumber5Up/100)

        bijBarAll.append(bijnumberAll/100)
        bijBar2.append(bijnumber2/100)
        bijBar3.append(bijnumber3/100)
        bijBar4.append(bijnumber4/100)
        bijBar5Up.append(bijnumber5Up/100)

        a = round(a + 0.01, 3)

    AverageaiBarAll.append(aiBarAll)
    AverageaiBar2.append(aiBar2)
    AverageaiBar3.append(aiBar3)
    AverageaiBar4.append(aiBar4)
    AverageaiBar5Up.append(aiBar5Up)

    AveragebijBarAll.append(bijBarAll)
    AveragebijBar2.append(bijBar2)
    AveragebijBar3.append(bijBar3)
    AveragebijBar4.append(bijBar4)
    AveragebijBar5Up.append(bijBar5Up)

    print(Counter)

for i in range(101):

    aiBarAllTicker = 0
    aiBar2Ticker = 0
    aiBar3Ticker = 0
    aiBar4Ticker = 0
    aiBar5UpTicker = 0

    bijBarAllTicker = 0
    bijBar2Ticker = 0
    bijBar3Ticker = 0
    bijBar4Ticker = 0
    bijBar5UpTicker = 0
    
    for j in range (AverageNNumber):
        aiBarAllTicker = aiBarAllTicker + AverageaiBarAll[j][i]
        aiBar2Ticker = aiBar2Ticker + AverageaiBar2[j][i]
        aiBar3Ticker = aiBar3Ticker + AverageaiBar3[j][i]
        aiBar4Ticker = aiBar4Ticker + AverageaiBar4[j][i]
        aiBar5UpTicker = aiBar5UpTicker + AverageaiBar5Up[j][i]

        bijBarAllTicker = bijBarAllTicker + AveragebijBarAll[j][i]
        bijBar2Ticker = bijBar2Ticker + AveragebijBar2[j][i]
        bijBar3Ticker = bijBar3Ticker + AveragebijBar3[j][i]
        bijBar4Ticker = bijBar4Ticker + AveragebijBar4[j][i]
        bijBar5UpTicker = bijBar5UpTicker + AveragebijBar5Up[j][i]
        
    AverageaiBarAllFinal.append(aiBarAllTicker/AverageNNumber)
    AverageaiBar2Final.append(aiBar2Ticker/AverageNNumber)
    AverageaiBar3Final.append(aiBar3Ticker/AverageNNumber)
    AverageaiBar4Final.append(aiBar4Ticker/AverageNNumber)
    AverageaiBar5UpFinal.append(aiBar5UpTicker/AverageNNumber)

    AveragebijBarAllFinal.append(bijBarAllTicker/AverageNNumber)
    AveragebijBar2Final.append(bijBar2Ticker/AverageNNumber)
    AveragebijBar3Final.append(bijBar3Ticker/AverageNNumber)
    AveragebijBar4Final.append(bijBar4Ticker/AverageNNumber)
    AveragebijBar5UpFinal.append(bijBar5UpTicker/AverageNNumber)


###### All plots
### Plot for pi(a)
y_pos = np.arange(len(alist))
colourAll = ['#2C3E50','#566573']
colour2 = ['#E74C3C','#EC7063']
colour3 = ['#6699CC','#256cb4']
colour4 = ['#2ECC71','#58D68D']
colour5Up = ['#F1C40F','#F4D03F']

plt.figure(1)
plt.bar(y_pos, AverageaiBarAllFinal, width = 1.0, align='center', color=colourAll, alpha=0.5)
plt.bar(y_pos, AverageaiBar2Final, width = 1.0, align='center', color=colour2, alpha=0.5)
plt.bar(y_pos, AverageaiBar3Final, width = 1.0, align='center', color=colour3, alpha=0.5)
plt.bar(y_pos, AverageaiBar4Final, width = 1.0, align='center', color=colour4, alpha=0.5)
plt.bar(y_pos, AverageaiBar5UpFinal, width = 1.0, align='center', color=colour5Up, alpha=0.5)
plt.xticks([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
           [0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00], rotation = 90)
plt.ylim((0,6))
plt.xlabel('a')
plt.ylabel(r'$\pi(a)$')
colors = {r'$\pi(a)$':'#2C3E50', r'$\pi(a|k=2)$':'#E74C3C', r'$\pi(a|k=3)$':'#6699CC', r'$\pi(a|k=4)$':'#2ECC71', r'$\pi(a|k\geq 5)$':'#F1C40F'}         
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
plt.legend(handles, labels)
plt.savefig('BA N=10000 Pi(a) Average Bar', bbox_inches='tight', dpi=300)

plt.figure(2)
plt.bar(y_pos, AveragebijBarAllFinal, width = 1.0, align='center', color=colourAll, alpha=0.5)
plt.bar(y_pos, AveragebijBar2Final, width = 1.0, align='center', color=colour2, alpha=0.5)
plt.bar(y_pos, AveragebijBar3Final, width = 1.0, align='center', color=colour3, alpha=0.5)
plt.bar(y_pos, AveragebijBar4Final, width = 1.0, align='center', color=colour4, alpha=0.5)
plt.bar(y_pos, AveragebijBar5UpFinal, width = 1.0, align='center', color=colour5Up, alpha=0.5)
plt.xticks([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
           [0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00], rotation = 90)
plt.ylim((0,6))
plt.xlabel('b')
plt.ylabel(r'$\pi(b)$')
colors = {r'$\pi(b)$':'#2C3E50', r'$\pi(b|k=2)$':'#E74C3C', r'$\pi(b|k=3)$':'#6699CC', r'$\pi(b|k=4)$':'#2ECC71', r'$\pi(b|k\geq 5)$':'#F1C40F'}         
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
plt.legend(handles, labels)
plt.savefig('BA N=10000 Pi(b) Average Bar', bbox_inches='tight', dpi=300)

plt.figure(3)
plt.grid()
plt.plot(y_pos, AverageaiBarAllFinal, color='#2C3E50')
plt.plot(y_pos, AverageaiBar2Final, color='#E74C3C')
plt.plot(y_pos, AverageaiBar3Final, color='#6699CC')
plt.plot(y_pos, AverageaiBar4Final, color='#2ECC71')
plt.plot(y_pos, AverageaiBar5UpFinal, color='#F1C40F')
plt.xticks([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
           [0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00], rotation = 90)
plt.ylim((0,6))
plt.xlabel('a')
plt.ylabel(r'$\pi(a)$')
colors = {r'$\pi(a)$':'#2C3E50', r'$\pi(a|k=2)$':'#E74C3C', r'$\pi(a|k=3)$':'#6699CC', r'$\pi(a|k=4)$':'#2ECC71', r'$\pi(a|k\geq 5)$':'#F1C40F'}         
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
plt.legend(handles, labels)
plt.savefig('BA N=10000 Pi(a) Average Line', bbox_inches='tight', dpi=300)

plt.figure(4)
plt.grid()
plt.plot(y_pos, AveragebijBarAllFinal, color='#2C3E50')
plt.plot(y_pos, AveragebijBar2Final, color='#E74C3C')
plt.plot(y_pos, AveragebijBar3Final, color='#6699CC')
plt.plot(y_pos, AveragebijBar4Final, color='#2ECC71')
plt.plot(y_pos, AveragebijBar5UpFinal, color='#F1C40F')
plt.xticks([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
           [0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00], rotation = 90)
plt.ylim((0,6))
plt.xlabel('b')
plt.ylabel(r'$\pi(b)$')
colors = {r'$\pi(b)$':'#2C3E50', r'$\pi(b|k=2)$':'#E74C3C', r'$\pi(b|k=3)$':'#6699CC', r'$\pi(b|k=4)$':'#2ECC71', r'$\pi(b|k\geq 5)$':'#F1C40F'}         
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
plt.legend(handles, labels)
plt.savefig('BA N=10000 Pi(b) Average Line', bbox_inches='tight', dpi=300)

plt.show()
