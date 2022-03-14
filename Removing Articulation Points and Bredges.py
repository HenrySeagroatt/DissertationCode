import networkx as nx
import random
from operator import itemgetter
import xlsxwriter

workbook = xlsxwriter.Workbook('Statistical Significance ER2 N=30.xlsx')
worksheet = workbook.add_worksheet()
### Creates the worksheet the data will be added to

n = 30
q = (1/15)
seed = 19959
### Conditions to create an Erdos Renyi Network with mean degree C=2 and N=30 nodes

NodeRandomOne = []
    ### Will be a list of the largest GCC's after one node is randomly removed
NodeRandomOnei = []
    ### Will be a list of the largest GCC's after one node is randomly removed and states which node has been removed
ArticulationOneMost = []
    ### Will be a list of the largest GCC's after the most significant articulation point is removed
ArticulationOneMosti = []
    ### Will be a list of the largest GCC's after the most significant articulation point is removed and states which node has been removed
ArticulationOneRandom = []
    ### Will be a list of the largest GCC's after a random articulation point is removed
ArticulationOneRandomi = []
    ### Will be a list of the largest GCC's after a random articulation point is removed and states which node has been removed
EdgeRandomOne = []
    ### Will be a list of the largest GCC's after one edge is randomly removed
EdgeRandomOnei = []
    ### Will be a list of the largest GCC's after one node is randomly removed and states which node has been removed
BredgeOneMost = []
    ### Will be a list of the largest GCC's after the most significant bredge is removed
BredgeOneMosti = []
    ### Will be a list of the largest GCC's after the most significant bredge is removed and states which edge has been removed
BredgeOneRandom = []
    ### Will be a list of the largest GCC's after the a random bredge is removed
BredgeOneRandomi = []
    ### Will be a list of the largest GCC's after the a random bredge is removed and states which edge has been removed

for i in range(1000):
    ### Randomly removes one node from the ER2 graph and states the size of its largest GCC
    G = nx.erdos_renyi_graph(n, q, seed=seed+i, directed=False) ### Generates ER2 network
    RandomValue = random.choice(list(G.nodes)) ### Randomly chooses a node
    G.remove_node(RandomValue) ### Removes the randomly chosen node
    NodeRandomOnei.append(tuple((RandomValue, len(max(nx.connected_components(G), key=len))))) ### Adds the node and size of the largest GCC on the cavity graph to a list
    NodeRandomOne.append(len(max(nx.connected_components(G), key=len))) ### Adds the size of the largest GCC on the cavity graph to a list

    ###Removes most significant articulation point from the ER2 graph and states the size of its largest GCC
    G = nx.erdos_renyi_graph(n, q, seed=seed+i, directed=False) ### Generates ER2 network
    ArticulationTemp = []
    for j in range(n):
        J = nx.erdos_renyi_graph(n, q, seed=seed+i, directed=False)
        if j in list(nx.articulation_points(J)):
            J.remove_node(j)
            ArticulationTemp.append(tuple((j, len(max(nx.connected_components(G), key=len))-len(max(nx.connected_components(J), key=len)))))
            ### Removes an articulation point and adds the point and size of the largest GCC on the cavity graph to a list
    G.remove_node(max(ArticulationTemp, key=itemgetter(1))[0])
    ### Removes the articulation point that results in the smallest largest GCC on the cavity graph to a list
    ArticulationOneMosti.append(tuple((max(ArticulationTemp, key=itemgetter(1))[0], len(max(nx.connected_components(G), key=len))))) ### Adds the articulation point and size of the largest GCC on the cavity graph to a list
    ArticulationOneMost.append(len(max(nx.connected_components(G), key=len))) ### Adds the size of the largest GCC on the cavity graph to a list

    ### Removes random articulation point from the ER2 graph and states the size of its largest GCC
    G = nx.erdos_renyi_graph(n, q, seed=seed+i, directed=False) ### Generates ER2 network
    RandomValue = random.choice(list(nx.articulation_points(G))) ### Randomly chooses one articulation point
    G.remove_node(RandomValue) ### Removes the randomly chosen articulation point
    ArticulationOneRandomi.append(tuple((RandomValue, len(max(nx.connected_components(G), key=len))))) ### Adds the articulation point and size of the largest GCC on the cavity graph to a list
    ArticulationOneRandom.append(len(max(nx.connected_components(G), key=len))) ### Adds the size of the largest GCC on the cavity graph to a list

    ### Randomly removes one edge from the ER2 graph and states the size of its largest GCC
    G = nx.erdos_renyi_graph(n, q, seed=seed+i, directed=False) ### Generates ER2 network
    RandomValue = random.choice(list(G.edges)) ### Randomly chooses an edge
    G.remove_edge(*RandomValue) ### Removes the randomly chosen edge
    EdgeRandomOnei.append(tuple((RandomValue, len(max(nx.connected_components(G), key=len)))))  ### Adds the edge and size of the largest GCC on the cavity graph to a list
    EdgeRandomOne.append(len(max(nx.connected_components(G), key=len))) ### Adds the size of the largest GCC on the cavity graph to a list

    ###Removes most significant bredge from the ER2 graph and states the size of its largest GCC
    G = nx.erdos_renyi_graph(n, q, seed=seed+i, directed=False) ### Generates ER2 network
    BredgeTemp = []
    for j in range(len(list(nx.bridges(G)))):
        J = nx.erdos_renyi_graph(n, q, seed=seed+i, directed=False)
        J.remove_edge(*list(nx.bridges(G))[j])
        BredgeTemp.append(tuple((list(nx.bridges(G))[j], len(max(nx.connected_components(G), key=len))-len(max(nx.connected_components(J), key=len)))))\
        ### Removes a bredge and adds the point and size of the largest GCC on the cavity graph to a list
    G.remove_edge(*max(BredgeTemp, key=itemgetter(1))[0])
    ### Removes the bredge that results in the smallest largest GCC on the cavity graph to a list
    BredgeOneMosti.append(tuple((max(BredgeTemp, key=itemgetter(1))[0], len(max(nx.connected_components(G), key=len))))) ### Adds the bredge and size of the largest GCC on the cavity graph to a list
    BredgeOneMost.append(len(max(nx.connected_components(G), key=len))) ### Adds the size of the largest GCC on the cavity graph to a list
 
    ### Removes random bredge from the ER2 graph and states the size of its largest GCC
    G = nx.erdos_renyi_graph(n, q, seed=seed+i, directed=False) ### Generates ER2 network
    RandomValue = random.choice(list(nx.bridges(G))) ### Randomly chooses one bredge
    G.remove_edge(*RandomValue) ### Removes the randomly chosen bredge
    BredgeOneRandomi.append(tuple((RandomValue, len(max(nx.connected_components(G), key=len))))) ### Adds the bredge and size of the largest GCC on the cavity graph to a list
    BredgeOneRandom.append(len(max(nx.connected_components(G), key=len))) ### Adds the size of the largest GCC on the cavity graph to a list
    
    print("Number of networks analysed...",i)
    ### A way of visualising how much of the code has been executed

worksheet.write(0, 0, 'Size of GCC after randomly removing one node')
worksheet.write_column(1, 0, NodeRandomOne)
worksheet.write(0, 1, 'Size of GCC after removing the most significant articulation point')
worksheet.write_column(1, 1, ArticulationOneMost)
worksheet.write(0, 2, 'Size of GCC after randomly removing one articulation point')
worksheet.write_column(1, 2, ArticulationOneRandom)
worksheet.write(0, 3, 'Size of GCC after randomly removing one edge')
worksheet.write_column(1, 3, EdgeRandomOne)
worksheet.write(0, 4, 'Size of GCC after removing the most significant bredge')
worksheet.write_column(1, 4, BredgeOneMost)
worksheet.write(0, 5, 'Size of GCC after randomly removing one bredge')
worksheet.write_column(1, 5, BredgeOneRandom)
workbook.close()
