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

Number = 100

Coefficient = nsum(lambda k:(k**(-3)), [2,1000])

k2 = nsum(lambda k:(k**2)*(1/Coefficient)*(k**(-3)), [2,1000])
k1 = nsum(lambda k:(k)*(1/Coefficient)*(k**(-3)), [2,1000])
critical = (k2-k1)/k1


start = datetime.now().time()
print("start time =", start)

GTilde = []
for i in range (Number):
    rng = default_rng(i)
    GTilde.append(rng.random())
    ### Randomly generates our initial conditions

G = []
A = []
B = []

ValuesOfKUStep = []
DistributionOfKUStep = []
for k in range(2,Number):
    ValuesOfKUStep.append(k)
    DistributionOfKUStep.append((k/k1)*(1/Coefficient)*(k**(-3)))

ValuesOfKMStep = []
DistributionOfKMStep = []
for k in range(2,Number):
    ValuesOfKMStep.append(k)
    DistributionOfKMStep.append((1/Coefficient)*(k**(-3)))

BlankArray = []
for i in range (1000):
    BlankArray.append([])
Array1 = np.array(BlankArray)
Array2 = np.array(BlankArray)
Array3 = np.array(BlankArray)

q = 1

while q >= 0:

    ### 500 initialisation sweeps with 1000 steps per sweep
    if q == 1:
        for j in range(Number):
            for i in range (Number):
                RandomValueOfKUStep = next(iter(random.choices(ValuesOfKUStep,DistributionOfKUStep))) - 1
                while RandomValueOfKUStep <= 2:
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

    ### 500 equlibration sweeps with 1000 steps per sweep
    for j in range (Number):
        for i in range (Number):
            RandomValueOfKUStep = next(iter(random.choices(ValuesOfKUStep,DistributionOfKUStep))) - 1
            while RandomValueOfKUStep <= 2:
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

    ### 500 nm sweeps with 500 usteps and 1000 m steps per sweep
    for j in range (Number):
        for i in range (Number):
            ### One update step
            RandomValueOfKUStep = next(iter(random.choices(ValuesOfKUStep,DistributionOfKUStep))) - 1
            while RandomValueOfKUStep <= 2:
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
            ### Chooses a random k according to the degree distribution given by \frac{k}{c}p_{k}

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

    ### Numpy arrays for heatmaps.
    pp = 1
    ArrayColumnList1 = []
    ArrayColumnList2 = []
    ArrayColumnList3 = []
    while pp > 0:
        Tally1 = 0
        Tally2 = 0
        Tally3 = 0
        ArrayElement1 = []
        ArrayElement2 = []
        ArrayElement3 = []
        for i in G:
            if pp - 0.001 < i <= pp:
                Tally1 = Tally1 + 1
            else:
                pass
        for i in A:
            if pp - 0.001 < i <= pp:
                Tally2 = Tally2 + 1
            else:
                pass
        for i in B:
            if pp - 0.001 < i <= pp:
                Tally3 = Tally3 + 1
            else:
                pass
        Tally1 = math.sqrt(Tally1) / (1 + math.sqrt(Tally1))
        Tally2 = math.sqrt(Tally2) / (1 + math.sqrt(Tally2))
        Tally3 = math.sqrt(Tally3) / (1 + math.sqrt(Tally3))
        ArrayElement1.append(Tally1)
        ArrayElement2.append(Tally2)
        ArrayElement3.append(Tally3)
        ArrayColumnList1.append(ArrayElement1)
        ArrayColumnList2.append(ArrayElement2)
        ArrayColumnList3.append(ArrayElement3)
        pp = round(pp - 0.001, 3)
    ArrayColumn1 = np.array(ArrayColumnList1)
    ArrayColumn2 = np.array(ArrayColumnList2)
    ArrayColumn3 = np.array(ArrayColumnList3)
    Array1 = np.append(Array1, ArrayColumn1, axis = 1)
    Array2 = np.append(Array2, ArrayColumn2, axis = 1)
    Array3 = np.append(Array3, ArrayColumn3, axis = 1)
    
    G = []
    A = []
    B = []

    onestep = datetime.now().time()
    print(q, "time =", onestep)

    q = round(q - 0.001, 3)

### Array for heatmap for the probability distribution of g in the thermodynamic limit
CorrectedArray1 = np.flip(Array1,1)
SaveData1 = asarray(CorrectedArray1)
savetxt('array1.csv', SaveData1, delimiter=',')

### Array for heatmap for the probability distribution of a in the thermodynamic limit
CorrectedArray2 = np.flip(Array2,1)
SaveData2 = asarray(CorrectedArray2)
savetxt('array2.csv', SaveData2, delimiter=',')

### Array for heatmap for the probability distribution of b in the thermodynamic limit
CorrectedArray3 = np.flip(Array3,1)
SaveData3 = asarray(CorrectedArray3)
savetxt('array3.csv', SaveData3, delimiter=',')

### Tickers for heatmaps
x = ['','0.00','0.05','0.10','0.15','0.20','0.25','0.30','0.35','0.40','0.45','0.50','0.55','0.60','0.65','0.70','0.75','0.80','0.85','0.90','0.95','1.00']
y = ['','1.00','0.95','0.90','0.85','0.80','0.75','0.70','0.65','0.60','0.55','0.50','0.45','0.40','0.35','0.30','0.25','0.20','0.15','0.10','0.05','0.00']

### Heatmap for the probability distribution of g in the thermodynamic limit
plt.figure(1)
LoadData1 = loadtxt('array1.csv', delimiter=',')
ax1 = sns.heatmap(data=LoadData1)
ax1.xaxis.set_major_locator(ticker.MultipleLocator(50))
ax1.xaxis.set_major_formatter(ticker.ScalarFormatter())
ax1.set_xticklabels(x)
ax1.set_xlabel('p')
ax1.yaxis.set_major_locator(ticker.MultipleLocator(50))
ax1.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax1.set_yticklabels(y)
ax1.set_ylabel(r'$\pi (g)$')
plt.savefig('Thermodynamic Probabilities', bbox_inches='tight', dpi=300)

### Heatmap for the probability distribution of a in the thermodynamic limit
plt.figure(2)
LoadData2 = loadtxt('array2.csv', delimiter=',')
ax2 = sns.heatmap(data=LoadData2)
ax2.xaxis.set_major_locator(ticker.MultipleLocator(50))
ax2.xaxis.set_major_formatter(ticker.ScalarFormatter())
ax2.set_xticklabels(x)
ax2.set_xlabel('p')
ax2.yaxis.set_major_locator(ticker.MultipleLocator(50))
ax2.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax2.set_yticklabels(y)
ax2.set_ylabel(r'$\pi (a)$')
plt.savefig('Thermodynamic Articulation Point Probabilities', bbox_inches='tight', dpi=300)

### Heatmap for the probability distribution of b in the thermodynamic limit
plt.figure(3)
LoadData3 = loadtxt('array3.csv', delimiter=',')
ax3 = sns.heatmap(data=LoadData3)
ax3.xaxis.set_major_locator(ticker.MultipleLocator(50))
ax3.xaxis.set_major_formatter(ticker.ScalarFormatter())
ax3.set_xticklabels(x)
ax3.set_xlabel('p')
ax3.yaxis.set_major_locator(ticker.MultipleLocator(50))
ax3.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax3.set_yticklabels(y)
ax3.set_ylabel(r'$\pi (b)$')
plt.savefig('Thermodynamic Bredge Probabilities', bbox_inches='tight', dpi=300)

plt.show()
