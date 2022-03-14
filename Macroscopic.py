import networkx as nx
from mpmath import *
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

start = datetime.now().time()
print("Start time =", start)

mp.dps = 3
n = 40
q = 1/20
### Conditions for an ER2 graph

### Checks that the probability distribution adds up to 1
#print(nsum(lambda k:((((n*q)**k)*((nsum(lambda r: 1/fac(r), [0,inf]))**(-(n*q))))/fac(k)),[0,inf]))

### Finding critical value
k2 = nsum(lambda k:(k**2)*((((n*q)**k)*((mp.e)**(-(n*q))))/fac(k)), [0,inf])
k1 = nsum(lambda k:(k)*((((n*q)**k)*((mp.e)**(-(n*q))))/fac(k)), [0,inf])
critical = (k2-k1)/k1

### Generates a graph of one instance of gtilde cobwebbing and one graph of three instances of gtilde cobwebbing
p = 0.25
x = 0.95 ### Any initial condition, just needs to be different from 0 (the trivial solution)
y = 0.1 ### (arbitrary, good as long as its not the same as x)
while y != x:
    x = round(nsum(lambda k:((k/(n*q))*((((n*q)**k)*((mp.e)**(-(n*q))))/fac(k))*(1-(1-(p*x))**(k-1))),[1,inf]),3)
    y = round(nsum(lambda k:((k/(n*q))*((((n*q)**k)*((mp.e)**(-(n*q))))/fac(k))*(1-(1-(p*x))**(k-1))),[1,inf]),3)

i = 0
xlist1 = []
ylist1 = []
while i <= 1:
    xlist1.append(i)
    ylist1.append(round(nsum(lambda k:((k/(n*q))*((((n*q)**k)*((mp.e)**(-(n*q))))/fac(k))*(1-(1-(p*i))**(k-1))),[1,inf]),3))
    i = round(i+0.01,2)
    ### Plots g tilde

### Generates a graph of one instance of gtilde cobwebbing and one graph of three instances of gtilde cobwebbing
p = 0.70
x = 0.95
y = 0.1 
while y != x:
    x = round(nsum(lambda k:((k/(n*q))*((((n*q)**k)*((mp.e)**(-(n*q))))/fac(k))*(1-(1-(p*x))**(k-1))),[1,inf]),3)
    y = round(nsum(lambda k:((k/(n*q))*((((n*q)**k)*((mp.e)**(-(n*q))))/fac(k))*(1-(1-(p*x))**(k-1))),[1,inf]),3)

i = 0
xlist2 = []
ylist2 = []
while i <= 1:
    xlist2.append(i)
    ylist2.append(round(nsum(lambda k:((k/(n*q))*((((n*q)**k)*((mp.e)**(-(n*q))))/fac(k))*(1-(1-(p*i))**(k-1))),[1,inf]),3))
    i = round(i+0.01,2)
    ### Plots g tilde

### Generates a graph of one instance of gtilde cobwebbing and one graph of three instances of gtilde cobwebbing
p = 0.90
x = 0.95 
y = 0.1
while y != x:
    x = round(nsum(lambda k:((k/(n*q))*((((n*q)**k)*((mp.e)**(-(n*q))))/fac(k))*(1-(1-(p*x))**(k-1))),[1,inf]),3)
    y = round(nsum(lambda k:((k/(n*q))*((((n*q)**k)*((mp.e)**(-(n*q))))/fac(k))*(1-(1-(p*x))**(k-1))),[1,inf]),3)
print(y)

i = 0
xlist3 = []
ylist3 = []
while i <= 1:
    xlist3.append(i)
    ylist3.append(round(nsum(lambda k:((k/(n*q))*((((n*q)**k)*((mp.e)**(-(n*q))))/fac(k))*(1-(1-(p*i))**(k-1))),[1,inf]),3))
    i = round(i+0.01,2)
    ### Plots g tilde

plt.figure(1)
plt.plot(xlist3, xlist3, 'black', label = r'y = $\tilde{g}$')
plt.plot(xlist3, ylist3, 'navy', label = r'y = F($\tilde{g}$)')
plt.plot(0, 0, marker=".", markersize=10, markeredgecolor='#FF8080', markerfacecolor='#FF8080')
plt.plot(y, y, marker=".", markersize=10, markeredgecolor='#FF8080', markerfacecolor='#FF8080')
plt.xlabel(r'$\tilde{g}_{t}$')
plt.ylabel(r'$\tilde{g}_{t+1}$')
plt.grid()
plt.savefig('ER2 GTilde', bbox_inches='tight', dpi=300)
### Plots g tilde for p=0.9

plt.figure(2)
plt.plot(xlist3, xlist3, 'black', label = r'y = $\tilde{g}$')
plt.plot(xlist1, ylist1, 'red', label = r'y = F($\tilde{g}$) with p = 0.25')
plt.plot(xlist2, ylist2, 'green', label = r'y = F($\tilde{g}$) with p = 0.70')
plt.plot(xlist3, ylist3, 'blue', label = r'y = F($\tilde{g}$) with p = 0.90')
plt.xlabel(r'$\tilde{g}$')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.savefig('ER2 GTilde Multiple', bbox_inches='tight', dpi=300)
### Plots g tilde for p = 0.25, 0.70, 0.90


p = 1
plist = []
zlist = []
while p >= 0:
    ### Iterates through p in [0,1]
    plist.append(p)
    Iteration = 1
    x = 0.95 ### Any initial condition, just needs to be different from 0 (the trivial solution)
    y = 0.1 ### (arbitrary, good as long as its not the same as x)
    if p == 0.5:
        while y != x:
            x = round(nsum(lambda k:(k/(n*q))*((((n*q)**k)*(mp.e**(-(n*q))))/fac(k))*(1-(1-(p*x))**(k-1)),[1,inf]),6)
            y = round(nsum(lambda k:(k/(n*q))*((((n*q)**k)*(mp.e**(-(n*q))))/fac(k))*(1-(1-(p*x))**(k-1)),[1,inf]),6)
            Iteration = Iteration + 1
        zlist.append(nsum(lambda k:((((n*q)**k)*(mp.e**(-(n*q))))/fac(k))*(1-(1-(p*y))**(k)),[0,inf]))
    else:
        while y!= x:
            x = nsum(lambda k:(k/(n*q))*((((n*q)**k)*(mp.e**(-(n*q))))/fac(k))*(1-(1-(p*x))**(k-1)),[1,inf])
            y = nsum(lambda k:(k/(n*q))*((((n*q)**k)*(mp.e**(-(n*q))))/fac(k))*(1-(1-(p*x))**(k-1)),[1,inf])
            Iteration = Iteration + 1
        zlist.append(nsum(lambda k:((((n*q)**k)*(mp.e**(-(n*q))))/fac(k))*(1-(1-(p*y))**(k)),[0,inf]))
    ### Cobwevs for each value of p

    if p*critical == 1:
        pc = p
        print("Critical probability", pc)
    else:
        pass
    ### Identifies the critical point
    print("Loading...", p)
    p = round(p - 0.01, 2)

end = datetime.now().time()
print("End time =", end)

plt.figure(3)
plt.ylabel(r'$\bar{g}$')
plt.xlabel('p')
plt.plot(plist, zlist, 'black')
plt.plot(pc, 0, marker=".", markersize=10, markeredgecolor='#FF8080', markerfacecolor='#FF8080')
plt.grid()
plt.savefig('ER2 GBar', bbox_inches='tight', dpi=300)
### Plot for g bar

plt.show()
