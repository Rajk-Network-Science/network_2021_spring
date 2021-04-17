import pandas as pd
import numpy as np
import itertools
import networkx as nx
from pyvis import network as net
from IPython.core.display import display, HTML

# node_features=pd.read_csv("attributes.csv")
# edge_features=pd.read_csv("edge_list_final.csv")


def generate_data(node_features,edge_features):
    '''
    data: node attributes
    data2: edge list
    '''
    node_features.columns=['Origin','Year','Origin_latitude','Origin_longitude','stock_migration']
    node_features = node_features.set_index("Origin")
    node_features=node_features.drop(['Year','Origin_latitude','Origin_longitude'], axis=1)
    
    edge_features=edge_features.drop(['Unnamed: 0','Year','Stock','Origin_latitude','Origin_longitude','Destination_latitude','Destination_longitude'], axis=1)
    edge_features.columns=['origin','destination','migration']
    
    node_features["display_nodesize"] = (
        node_features["stock_migration"]
        .pipe(lambda s: np.log(s.apply(lambda x: max(1,x))))
        .pipe(lambda s: s / np.nanmean(s) * 100)
    )
    edge_features["display_edgesize"] = (
        edge_features["migration"]
        .pipe(lambda s: s / np.nanmean(s))
    )
    
    edge_features = (
        node_features.reset_index()[["Origin"]]
        .pipe(
            lambda df: edge_features.merge(
                df, left_on="origin", right_on="Origin", how="right"
            )
            .drop("Origin", axis=1)
            .merge(df, left_on="destination", right_on="Origin", how="right")
        )
        .dropna(how="any")
        .drop(["Origin"], axis=1)
    )
    return node_features,edge_features

def graf_vizu(edge_features,node_features, logarithm=True):
    '''
    edge features oszlopai: origin, destination, flow migration
    node features oszlopai: stock migration
    '''
    mig_net = net.Network(height='750px', width='100%', bgcolor='#222222', font_color='white', notebook=True)
    # set the physics layout of the network
    mig_net.barnes_hut()
    #Add nodes
    for i, r in node_features.iterrows():
        if logarithm:
            mig_net.add_node(i, i, title=i, size=r["display_nodesize"])
        else:
            mig_net.add_node(i, i, title=i, size=r["stock_migration"])
    #Add edges
    for i, r in edge_features.iterrows():
        if logarithm:
            mig_net.add_edge(r["origin"], r["destination"], width=r["display_edgesize"])
        else:
            mig_net.add_edge(r["origin"], r["destination"], width=r["migration"])
    return mig_net