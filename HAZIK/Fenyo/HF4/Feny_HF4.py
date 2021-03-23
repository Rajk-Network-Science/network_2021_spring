import pandas as pd
import numpy as np
import matplotlib as plt
import networkx as nx
import random
import time

# Random seed for reproduction
random.seed(11)

# Create base ER graph
ER = nx.erdos_renyi_graph(20,0.2, seed = 11)

# Link selection model
def link_selection(G, n):
    '''
    Adds n random new edges to networkx object G, with edges calclutated like this
    - choose a random edge from G
    - choose one of the nodes
    - do this 3 times
    - the new node will connect to these 3 nodes
    '''
    H = G
    for i in range(n):
        H.add_node(1000+i)
        for j in range(3):
            H.add_edge(1000+i, random.choice(random.choice(list(H.edges))))
    
    return H

# Copy model

# BA model



