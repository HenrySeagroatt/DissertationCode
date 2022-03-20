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
p = 15000
for i in NumberOfNodes:
    NLogNList.append((1/p)*i*(ln(i)/ln(ln(i))))
    ### Creates the values used to plot aND(N)

AverageTime = loadtxt('AverageTime For BA.csv', delimiter=',')
### Loads the generated data.

plt.figure(1)
plt.plot(NumberOfNodes, NLogNList, 'black', label=r'$\frac{cNln(N)}{ln(ln(N))}$')
plt.plot(NumberOfNodes, AverageTime, 'red', label='Time taken to solve an \nBarabási Albert model \nwith m = 2 and N nodes')
plt.xlabel('Number of Nodes (N)')
plt.ylabel('Time (Seconds)')
plt.legend()
plt.grid()
plt.savefig('ER2 Averaged N=5000', bbox_inches='tight', dpi=300)
plt.show()
### Plots the data

