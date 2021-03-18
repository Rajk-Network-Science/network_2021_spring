import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import collections

df=pd.read_csv("musae_ENGB_edges.csv",delimiter=",")
G=nx.from_pandas_edgelist(df,"from","to")
group_by1=df.groupby(["from"]).count().sort_values(by=["to"],ascending=False)
x=group_by1["to"]

def alap_info(G):
    return print(nx.info(G))

def átmérő(G):
    return nx.diameter(G)

def átlagos_legrövidebb_út(G):
    return nx.average_shortest_path_length(G)

def átlagos_fokszám(x):
    return np.average(x)

def fokszámeloszlás_hist(x):
    plt.hist(x, density=False, range=(0,60), bins=100)
    plt.title("Fokszámeloszlás")
    plt.xlabel("Fokszám (bins=100)")
    plt.ylabel("Gyakoriság")
    plt.show()







