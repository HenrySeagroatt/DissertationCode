import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpmath import *
import random
import xlsxwriter

workbook = xlsxwriter.Workbook('Correctly Identifying.xlsx')
worksheet = workbook.add_worksheet()
### Creates a worksheet to write the data to

n = 1000
q = 1/500
### Variables used to specify the ER network will have mean degree c = 2

ArticulationList1 = []
### Number of articulation points identified by Networkx
ArticulationList2 = []
### Number of nodes my algorithm identifies that are articulation points according to Networkx
ArticulationList3 = []
### Number of articulation points according to Networkx that my algorithm fails to identify
ArticulationList4 = []
### Number of points my algorithm says are articulation points that aren't according to Networkx
BredgeList1 = []
### Number of bredges identified by Networkx
BredgeList2 = []
### Number of edges my algorithm identifies that are bredges according to Networkx
BredgeList3 = []
### Number of bredges according to Networkx that my algorithm fails to identify
BredgeList4 = []
### Number of points my algorithm says are bredges that aren't according to Networkx
CounterList = []
### Specifies the seed of the generated network

for counter in range(1000):

    CounterList.append(counter)

    G = nx.erdos_renyi_graph(n,q, seed=counter, directed=False)
    ### Generates a new random ER2 Graph for N = 1000
    
    p = 1
    ### States that all nodes are kept in a single realisation of the percolation process
    
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
        maxvalue = round(max(maxlist), 3)
        ### This iterates until the values of gji don't change by more than three decimal places.        

        ###### Sets the gjiold to the newly calculated gjinew for the next iteration, giving a new initial condition
        gjiold = {}
        for i in list(G.nodes):
            for j in list(G.adj[i]):
                gjiold["g{0}old{1}".format(j,i)] = gjinew["g{0}new{1}".format(j,i)]

    ###### Calculates values of b_{ij} and adds them to a list to compare them, to the known bredges.
    bij = {}
    bijList = []
    for i in list(G.nodes):
        for j in list(G.adj[i]):
            if i > j:
                ### Calculting the bredge probability
                bij["{0}b{1}".format(i,j)] = 1 - gjinew["g{0}new{1}".format(i,j)]*gjinew["g{0}new{1}".format(j,i)]
                ### If bij = 1 (i.e is an edge) we will add it to a list of calculated bredges
                if bij["{0}b{1}".format(i,j)] == 1:
                    bijList.append((j,i))

    ###### Calculates values of a_{i} and adds them to a list to compare to the known articulation points.
    ai = {}
    aiList = []
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
        if ai["a{0}".format(i)] == 1:
            aiList.append(i)

    ###### Tally data for articulation points
    Tally1Correct = 0
    Tally1Missed = 0
    Tally1Incorrect = 0
    for i in list(aiList):
        if i in list(nx.articulation_points(G)):
            Tally1Correct = Tally1Correct + 1
            ### Counts the number of articulation points the above algorithm calculates that are also in the list of articulation points according to Network's algorithms
        else:
            Tally1Incorrect = Tally1Incorrect + 1
            ### Counts the number of articulation points calculated using the Network's algorithm that the above algorithm failed to identify
    for i in list(nx.articulation_points(G)):
        if i in list(aiList):
            pass
        else:
            Tally1Missed = Tally1Missed + 1
            ### Counts the number of articulation points the above algorithm calculates that are not articulation points according to Network's algorithms
    ArticulationList1.append(len(list(nx.articulation_points(G))))
    ArticulationList2.append(Tally1Correct)
    ArticulationList3.append(Tally1Missed)
    ArticulationList4.append(Tally1Incorrect)

    ###### Tally data for bredges
    Tally2Correct = 0
    Tally2Missed = 0
    Tally2Incorrect = 0
    for i in list(bijList):
        if i in list(nx.bridges(G)):
            Tally2Correct = Tally2Correct + 1
            ### Counts the number of bredges the above algorithm calculates that are also in the list of bridges according to Network's algorithms
        else:
            Tally2Incorrect = Tally2Incorrect + 1
            ### Counts the number of bridges calculated using the Network's algorithm that the above algorithm failed to identify
    for i in list(nx.bridges(G)):
        if i in list(bijList):
            pass
        else:
            Tally2Missed = Tally2Missed + 1
            ### Counts the number of bredges the above algorithm calculates that are not bridges according to Network's algorithms
    BredgeList1.append(len(list(nx.bridges(G))))
    BredgeList2.append(Tally2Correct)
    BredgeList3.append(Tally2Missed)
    BredgeList4.append(Tally2Incorrect)

    print("Number of networks analysed...", counter)
    ### A way of visualising how quickly the programme is running

### Writes the collected data onto a spreadsheet
worksheet.write(0, 0, 'Number of articulation points')
worksheet.write_column(1, 0, ArticulationList1)
worksheet.write(0, 1, 'Number of correctly identified articulation points')
worksheet.write_column(1, 1, ArticulationList2)
worksheet.write(0, 2, "Number of articualtion points that it didn't identify")
worksheet.write_column(1, 2, ArticulationList3)
worksheet.write(0, 3, "Number of nodes that aren't articulation points that it said were")
worksheet.write_column(1, 3, ArticulationList4)
worksheet.write(0, 4, 'Number of bredges')
worksheet.write_column(1, 4, BredgeList1)
worksheet.write(0, 5, 'Number of correctly identified bredges')
worksheet.write_column(1, 5, BredgeList2)
worksheet.write(0, 6, "Number of bredges that it didn't identify")
worksheet.write_column(1, 6, BredgeList3)
worksheet.write(0, 7, "Number of nodes that aren't bredges that it said were")
worksheet.write_column(1, 7, BredgeList4)
worksheet.write(0, 8, "Seed")
worksheet.write_column(1, 8, CounterList)
workbook.close()
