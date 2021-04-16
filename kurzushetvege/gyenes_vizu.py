import pandas as pd
import numpy as np
import itertools
import networkx as nx
from pyvis import network as net
from IPython.core.display import display, HTML

list_of_countries=["a","b","c","d"]
node_sizes=[20,5,132,18]
node_features=pd.DataFrame(index=list_of_countries,data=node_sizes)
edges_index=list(itertools.combinations(list_of_countries, 2))
edge_values=np.random.rand(len(edges_index),1)
edge_features=pd.DataFrame(index=pd.MultiIndex.from_tuples(edges_index, names=('origin', 'destination')), data=edge_values)
edge_features.columns=["migration"]
node_features.columns=["stock_migration"]
edge_features=edge_features.reset_index()

def vizu(edge_features,node_features):
    '''
    edge features oszlopai: origin, destination, flow migration
    node features oszlopai: stock migration
    '''
    mig_net = net.Network(height='750px', width='100%', bgcolor='#222222', font_color='white', notebook=True)
    # set the physics layout of the network
    mig_net.barnes_hut()
    edge_data = zip(edge_features["origin"], edge_features["destination"], edge_features["migration"])
    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]
    
        mig_net.add_node(src, src, title=src, size=int(node_features.loc[src,"stock_migration"]))
        mig_net.add_node(dst, dst, title=dst, size=int(node_features.loc[dst,"stock_migration"]))
        mig_net.add_edge(src, dst, value=w)
    return mig_net