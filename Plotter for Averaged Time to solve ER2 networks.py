import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpmath import *
import time
from numpy import loadtxt

NumberOfNodes = []
for i in range(1,51):
    NumberOfNodes.append(i*100)
### Creates a list of numbers with difference of 100

NLogNList = []
a = 35500
for i in NumberOfNodes:
    NLogNList.append((1/a)*i*(log(i)/log(2)))
### Creates the values used to plot aND(N)

AverageTime = loadtxt('AverageTime.csv', delimiter=',')
### Loads the generated data.

plt.figure(1)
plt.plot(NumberOfNodes, NLogNList, 'black', label='aNln(N)')
plt.plot(NumberOfNodes, AverageTime, 'red', label='Time taken to solve an \nErdös Rényi network with \nmean degree c = 2 \nand N nodes')
plt.xlabel('Number of Nodes (N)')
plt.ylabel('Time (Seconds)')
plt.legend()
plt.grid()
plt.savefig('ER2 Averaged N=5000', bbox_inches='tight', dpi=300)
plt.show()
### Plots the data
