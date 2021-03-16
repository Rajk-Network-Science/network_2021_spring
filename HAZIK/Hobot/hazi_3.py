import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def graph_objektum(x):
    df=pd.read_csv(x ,delimiter=',')
    return nx.from_pandas_edgelist(df, "node_1", "node_2")


def deskriptiv(G):
    print("Number of nodes:", G.number_of_nodes() )
    print("Number of egdes:", G.number_of_edges() )
    print("Average degree:",2*len(G.edges)/len(G.nodes))
    print("Diameter:", nx.diameter(G))
    print("Average shortest path", nx.average_shortest_path_length(G))
    
def fokszam(G):
    node_list=[]
    degree_list=[]
    for node in G.nodes():
        node_list.append(node)
    for degree in G.degree():
        degree_list.append(degree[1])
    return pd.Series(degree_list, index = node_list)

def fokszameloszlas(df):
    df.sort_values(ascending=False).value_counts()

    plt.figure(figsize=(20,10))
    plt.hist(df, bins=100, color="orange", log=True)
    plt.title("Fokszámeloszlás", fontsize=32)
    plt.xlabel("Fokszámok (darab)", fontsize=20)
    plt.ylabel("A foszámok gyakoriságának logaritmusa", fontsize=20)
        
        
        