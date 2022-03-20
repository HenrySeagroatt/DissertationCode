import networkx as nx
import random
from mpmath import *
import numpy as np
from numpy import asarray
from numpy import savetxt
from numpy import loadtxt
from numpy.random import default_rng
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime
import math
from collections import Counter


### Imports SNAP data and reads the edge list
F = nx.read_edgelist('facebook_combined.txt', create_using=nx.Graph(), nodetype=int)

### List of the degrees of each node in the network
DegreeList = []
for i in F.nodes:
    DegreeList.append(F.degree[i])

### Sorts the list to ascend numberically
DegreeList.sort()

### Counts the number of distinct elements in the degree list
ListDistinctDegrees = []
for i in Counter(DegreeList).keys():
    ListDistinctDegrees.append(i)

### Calculates the probability of a node to have a certain degree
ListDistinctDegreesProbability = []
for i in Counter(DegreeList).values():
    ListDistinctDegreesProbability.append(i/len(list(F.nodes)))

### Simulations
GTilde = []
for i in range (1100):
    rng = default_rng(i)
    GTilde.append(rng.random())
    ### Randomly generates our initial conditions

G = []
A = []
B = []
AverageA = []
AverageB = []
PList = []

c = 0
for i in range(len(list(ListDistinctDegrees))):
    c = c + (ListDistinctDegrees[i] * ListDistinctDegreesProbability[i])

ValuesOfKUStep = []
ValuesOfKMStep = []
DistributionOfKUStep = []
DistributionOfKMStep = []
for i in range(len(list(ListDistinctDegrees))):
    ValuesOfKUStep.append(ListDistinctDegrees[i])
    ValuesOfKMStep.append(ListDistinctDegrees[i])
    DistributionOfKUStep.append((ListDistinctDegrees[i]/c)*ListDistinctDegreesProbability[i])
    DistributionOfKMStep.append(ListDistinctDegreesProbability[i])
    
q = 1

while q >= 0:

    PList.append(q)

    ### 500 initialisation sweeps with 1100 steps per sweep
    if q == 1:
        for j in range(500):
            for i in range (1100):
                RandomValueOfKUStep = next(iter(random.choices(ValuesOfKUStep,DistributionOfKUStep))) - 1
                while RandomValueOfKUStep == -1:
                    RandomValueOfKUStep = next(iter(random.choices(ValuesOfKUStep,DistributionOfKUStep))) - 1
                ReducedGTildeUStep = random.sample(GTilde, RandomValueOfKUStep)
                ### Chooses a random k according to the degree distribution

                templist = []
                for g in ReducedGTildeUStep:
                    templist.append(1-q*g)
                x = 1
                for y in templist:
                    x = x * y
                NewGTildeUStep = 1 - x
                GTilde.remove(GTilde[i])
                GTilde.insert(i,NewGTildeUStep)
                ### Solves values of g tilde using the random value of k

    ### 200 equlibration sweeps with 500 steps per sweep
    for j in range (500):
        for i in range (1100):
            RandomValueOfKUStep = next(iter(random.choices(ValuesOfKUStep,DistributionOfKUStep))) - 1
            while RandomValueOfKUStep == -1:
                RandomValueOfKUStep = next(iter(random.choices(ValuesOfKUStep,DistributionOfKUStep))) - 1
            ReducedGTildeUStep = random.sample(GTilde, RandomValueOfKUStep)
            ### Chooses a random k according to the degree distribution

            templist = []
            for g in ReducedGTildeUStep:
                templist.append(1-q*g)
            x = 1
            for y in templist:
                x = x * y
            NewGTildeUStep = 1 - x
            GTilde.remove(GTilde[i])
            GTilde.insert(i,NewGTildeUStep)
            ### Solves values of g tilde using the random value of k

    ### 500 nm sweeps with 1100 usteps and 1100 m steps per sweep
    for j in range (500):
        for i in range (1100):
            ### One update step
            RandomValueOfKUStep = next(iter(random.choices(ValuesOfKUStep,DistributionOfKUStep))) - 1
            while RandomValueOfKUStep == -1:
                RandomValueOfKUStep = next(iter(random.choices(ValuesOfKUStep,DistributionOfKUStep))) - 1
            ReducedGTildeUStep = random.sample(GTilde, RandomValueOfKUStep)
            ### Chooses a random k according to the degree distribution

            templist = []
            for g in ReducedGTildeUStep:
                templist.append(1-q*g)
            x = 1
            for y in templist:
                x = x * y
            NewGTildeUStep = 1 - x
            GTilde.remove(GTilde[i])
            GTilde.insert(i,NewGTildeUStep)
            ### Solves values of g tilde using the random value of k

            ### One measurement step to generate values for g
            RandomValueOfKMStep1 = next(iter(random.choices(ValuesOfKMStep,DistributionOfKMStep)))
            ReducedGTildeMStep1 = random.sample(GTilde, RandomValueOfKMStep1)
            ### Chooses a random k according to the degree distribution given by \frac{k}{c}p_{k}

            templist = []
            for g in ReducedGTildeMStep1:
                templist.append(1-q*g)
            x = 1
            for y in templist:
                x = x * y
            NewGMStep = 1 - x
            G.append(NewGMStep)
            ### Solves values of g using the random value of k

            ### One measurement step to generate values for a
            RandomValueOfKMStep2 = next(iter(random.choices(ValuesOfKUStep,DistributionOfKUStep)))
            ReducedGTildeMStep2 = random.sample(GTilde, RandomValueOfKMStep2)
            ### Chooses a random k according to the degree distribution given by \frac{k}{c}p_{k}

            if RandomValueOfKMStep2 < 2:
                pass
            else:
                templist1 = []
                templist2 = []
                for g in ReducedGTildeMStep2:
                    templist1.append(1-g)
                    templist2.append(1-q+q*g)
                z = 0
                for y in templist1:
                    z = z + y
                x = 1
                for y in templist2:
                    x = x * y
                NewGMStep = 1 - ((q*((1-q)**(RandomValueOfKMStep2 - 1)))*z) - x
                A.append(NewGMStep)
            ### Solves values of a using the random value of k

            ### One measurement step to generate values of b

            RandomValueOfKMStep3 = next(iter(random.choices(ValuesOfKUStep,DistributionOfKUStep)))
            ReducedGTildeMStep3 = random.sample(GTilde, RandomValueOfKMStep3)
            ### Chooses a random k according to the degree distribution given by \frac{k}{c}p_{k}

            templist = []
            for g in ReducedGTildeMStep3:
                templist.append(1-q*g)
            x = 1
            for y in templist:
                x = x * y
            NewGMStep1 = 1 - x

            RandomValueOfKMStep4 = next(iter(random.choices(ValuesOfKUStep,DistributionOfKUStep)))
            ReducedGTildeMStep4 = random.sample(GTilde, RandomValueOfKMStep4)

            templist = []
            for g in ReducedGTildeMStep4:
                templist.append(1-q*g)
            x = 1
            for y in templist:
                x = x * y
            NewGMStep2 = 1 - x

            z = 1 - (NewGMStep1*NewGMStep2)
            B.append(z)
            ### Solves values of b using the random value of k

    AverageAValue = 0
    for i in A:
        AverageAValue = AverageAValue + i
    AverageA.append(AverageAValue/len(list(A)))
    ### Averages values of simulated a's

    AverageBValue = 0
    for i in B:
        AverageBValue = AverageBValue + i
    AverageB.append(AverageBValue/len(list(B)))
    ### Averages values of simulated b's
    
    G = []
    A = []
    B = []

    onestep = datetime.now().time()
    print(q, "time =", onestep)

    q = round(q - 0.01, 2)

Averageai2 = asarray(AverageA)
savetxt('Averageai2.csv', Averageai2, delimiter=',')
Averagebij2 = asarray(AverageB)
savetxt('Averagebij2.csv', Averagebij2, delimiter=',')
### Saves the data
