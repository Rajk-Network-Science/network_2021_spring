# Packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import time

# Data

PATH = '../HF3/lasftm_asia/lastfm_asia_edges.csv'

'''
The source of the database: https://snap.stanford.edu/data/feather-lastfm-social.html
'''

# Functions

def generate_graph(path):
    '''
    Generates an NX Graph object from a csv data source
    csv must contain edges in a two column format (node1, node2)
    '''
    edges = pd.read_csv(path, sep = ',')
    G = nx.Graph(list(zip(edges.iloc[:,0], edges.iloc[:,1])))
    print('Successfully read graph from ', path)
    print('Number of nodes: ', G.number_of_nodes())
    print('Number of edges: ', G.number_of_edges(), '\n \n')
    return G
    
def plot_degree_dist(G):
    '''
    Plots the degree distribution of an NX Graph object
    '''
    fig,axes=plt.subplots(1,2,figsize=(15,5))

    axes[0].bar(x = np.arange(start = pd.Series([d for n, d in G.degree]).value_counts().sort_index().index.min(),
                        stop  = pd.Series([d for n, d in G.degree]).value_counts().sort_index().index.max()+1,
                        step  = 1),
                height = pd.Series(index=np.arange(start = pd.Series([d for n, d in G.degree]).value_counts().sort_index().index.min(),
                        stop  = pd.Series([d for n, d in G.degree]).value_counts().sort_index().index.max()+1,
                        step  = 1),
                    data=pd.Series([d for n, d in G.degree]).value_counts().sort_index().fillna(0)))
    axes[0].set_title('A gráf fokszámeloszlása')
    axes[0].set_xlabel('Fokszám')
    axes[0].set_ylabel('Frekvencia')
    
    axes[1].bar(x = np.arange(start = pd.Series([d for n, d in G.degree]).value_counts().sort_index().index.min(),
                        stop  = pd.Series([d for n, d in G.degree]).value_counts().sort_index().index.max()+1,
                        step  = 1),
                height = np.log(pd.Series(index=np.arange(start = pd.Series([d for n, d in G.degree]).value_counts().sort_index().index.min(),
                        stop  = pd.Series([d for n, d in G.degree]).value_counts().sort_index().index.max()+1,
                        step  = 1),
                    data=pd.Series([d for n, d in G.degree]).value_counts().sort_index().fillna(0))))
    axes[1].set_title('A gráf fokszámeloszlása logaritmikus skálán')
    axes[1].set_xlabel('Fokszám')
    axes[1].set_ylabel('Frekvencia logaritmusa')
    plt.show()
    
def avg_degree(G):
    '''
    Returns the average degree of an NX Graph object
    '''
    return sum([d for n, d in G.degree]) / len([d for n, d in G.degree])
    
def calc_diam(G):
    '''
    Calculates the diameter of an NX Graph object with the built in function of NX package
    '''
    return nx.algorithms.distance_measures.diameter(G)
    
def calc_avg_shortest(G):
    '''
    Calculates the average eccentricity of an NX Graph object with the built in function of NX package
    '''
    distances = nx.algorithms.distance_measures.eccentricity(G)
    return sum(list(distances.values())) / len(list(distances.values()))
    
def calc_clustering(G):
    '''
    Calculates the Average Clustering Coefficient of an NX Graph object using the built in function of NX package
    '''
    return nx.average_clustering(G)
    
def analyse(G):
    '''
    Runs the previous 4 analysing functions and draw 2 plots on an NX Graph object
    prints the elapsed time between calculations
    '''
    
    #Calculating
    t1 = time.perf_counter()
    print('The average degree in the graph is: ', avg_degree(G))
    t2 = time.perf_counter()
    print(f'Calculating this took {t2 - t1:0.4f} seconds \n \n')
    
    print('Diameter of network: ', calc_diam(G))
    t3 = time.perf_counter()
    print(f'Calculating this took {t3 - t2:0.4f} seconds \n \n')
    
    print('Average eccentricity: ', calc_avg_shortest(G))
    t4 = time.perf_counter()
    print(f'Calculating this took {t4 - t3:0.4f} seconds \n \n')
    
    print('Average Clustering Coefficient: ', calc_clustering(G))
    t5 = time.perf_counter()
    print(f'Calculating this took {t5 - t4:0.4f} seconds \n \n')
    
    #Plotting
    plot_degree_dist(G)
    
    plt.figsize = (50,50)
    nx.draw(G,
        node_size = 20,
        alpha = 0.3,
        with_labels = False)
    plt.title('A LastFM közösségi kapcsolatai')
    plt.show()
    
    t6 = time.perf_counter()
    print(f'Ended full analysis in {t6 - t1:0.4f} seconds')
    


