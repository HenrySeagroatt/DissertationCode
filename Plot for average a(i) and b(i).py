import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpmath import *
import time
from numpy import loadtxt
from numpy import asarray

Averageai = loadtxt('Averageai.csv', delimiter=',')
Averagebij = loadtxt('Averagebij.csv', delimiter=',')
AverageA = loadtxt('Averageai2.csv', delimiter=',')
AverageA2 = []
for i in AverageA:
    AverageA2.append(i)
AverageA2.reverse()
AverageB = loadtxt('Averagebij2.csv', delimiter=',')
AverageB2 = []
for i in AverageB:
    AverageB2.append(i)
AverageB2.reverse()
### Loads all the data, and flips the list of data points for simulated values of a_{i} and b_{ij} as they were incorrectly ordered initially.

plist = []
p = 0
while p <=1:
    plist.append(p)
    p = round(p + 0.01, 3)

y_pos = np.arange(len(plist))

plt.figure(1)
plt.plot(y_pos, Averageai, color='black', label='Facebook Ego Network')
plt.plot(y_pos, AverageA2, color='red', label='Randomized')
plt.legend()
plt.xticks([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
           [0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00], rotation = 90)
plt.xlabel('p')
plt.ylabel('a')
plt.grid()
plt.savefig('Facebook Ego Network Average a_{i}', bbox_inches='tight', dpi=300)
### Plots the graph for average values of a_{i}

plt.figure(2)
plt.plot(y_pos, Averagebij, color='black', label='Facebook Ego Network')
plt.plot(y_pos, AverageB2, color='red', label='Randomized')
plt.legend()
plt.xticks([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
           [0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00], rotation = 90)
plt.xlabel('p')
plt.ylabel('b')
plt.grid()
plt.savefig('Facebook Ego Network Average b_{ij}', bbox_inches='tight', dpi=300)
### Plots the graph for average values of b_{ij}

plt.show()
