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
p = 92000
for i in NumberOfNodes:
    NLogNList.append((1/p)*i*(log(i)/log(2)))
### Creates the values used to plot aND(N)

Time = loadtxt('Time N=5000.csv', delimiter=',')
### Loads the generated data.

plt.figure(1)
plt.plot(NumberOfNodes, NLogNList, 'black', label='aNln(N)')
plt.plot(NumberOfNodes, Time, 'red', label='Time taken to solve an \nErdös Rényi network with \nmean degree c = 2 \nand N nodes')
plt.xlabel('Number of Nodes (N)')
plt.ylabel('Time (Seconds)')
plt.legend()
plt.grid()
plt.savefig('ER2 N=5000', bbox_inches='tight', dpi=300)
plt.show()
### Plots the data
