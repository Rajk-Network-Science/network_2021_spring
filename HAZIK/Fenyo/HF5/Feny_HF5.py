import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import time
import gc
# from littleballoffur import SnowBallSampler - ez hibára fut
import Graph_Sampling

# Random seed for reproduction
random.seed(11)

# Read the data
'''
The source of this database: https://snap.stanford.edu/data/soc-Pokec.html
'''

DATAPATH = 'C:/Users/HP/Documents/02_CODING/KURZUS_Network/DATA/HF5'

def read_data_create_graph():
    # Read the two text files
    rels = pd.read_csv(DATAPATH + '/soc-pokec-relationships.txt', sep = '\t', header = None)
    people = pd.read_csv(DATAPATH + '/soc-pokec-profiles.txt', sep = '\t', names = [x.strip() for x in list(pd.read_csv(DATAPATH + '/column_names.csv', header = None)[0])], index_col = False).rename(columns = {'AGE' : 'age'})[['user_id', 'gender', 'age']]
    print('Data read successfully.')
    
    # Create the graph
    G = nx.Graph()
    G.add_edges_from(list(zip(rels[0], rels[1])))
    
    # Set attrubutes for gender and age
    nx.set_node_attributes(G, pd.Series(people.gender, index=people.user_id).to_dict(), 'gender')
    nx.set_node_attributes(G, pd.Series(people.age,    index=people.user_id).to_dict(), 'age')
    
    print('Graph created successfully. \n \n')
    print('The number of nodes is: ', G.number_of_nodes())
    print('The number of edges is: ', G.number_of_edges())
    print('The average degrre is: ', sum([d for n, d in G.degree]) / len([d for n, d in G.degree]))
    
    del rels, people
    gc.collect()
    print('Dropped garbage.')
    
    return G
    
def create_subgraph(G, n):
    sampler = Graph_Sampling.SRW_RWF_ISRW()
    subG = sampler.random_walk_sampling_simple(G, n)
    
    print('Subgraph created successfully. \n \n')
    print('The number of nodes is: ', subG.number_of_nodes())
    print('The number of edges is: ', subG.number_of_edges())
    print('The average degrre is: ', sum([d for n, d in subG.degree]) / len([d for n, d in subG.degree]))
    
    del G
    gc.collect()
    print('Dropped garbage.')
    
    return subG
    
    

    







