import pandas as pd
import numpy as np
import itertools
import networkx as nx
from pyvis import network as net
from IPython.core.display import display, HTML
import plotly.express as px

# node_features=pd.read_csv("attributes.csv")
# edge_features=pd.read_csv("edge_list_final.csv")


def generate_data(node_features,edge_features, node_size_multiplier, edge_weight_multiplier):
    '''
    data: node attributes
    data2: edge list
    '''
    node_features.columns=['Origin','Year','Origin_latitude','Origin_longitude','stock_migration']
    #node_features=node_features.loc[node_features['Year'] == 2017]
    node_features = node_features.set_index("Origin")
    node_features=node_features.drop(['Year','Origin_latitude','Origin_longitude'], axis=1)
    
    #edge_features=edge_features.loc[edge_features['Year'] == 2017]
    edge_features=edge_features.drop(['Year','Origin_latitude','Origin_longitude','Destination_latitude','Destination_longitude'], axis=1)
    edge_features.columns=['origin','destination','stock_migration','migration']
    
    node_features["display_nodesize"] = (
        node_features["stock_migration"]
        .pipe(lambda s: np.log(s.apply(lambda x: max(1,x))))
        .pipe(lambda s: s / np.nanmean(s) * node_size_multiplier)
    )
    edge_features["display_edgesize"] = (
        edge_features["migration"]
        .pipe(lambda s: s / np.nanmax(s) * edge_weight_multiplier)
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

def graf_vizu(edge_features,node_features, logarithm=True, node_size_multiplier = 30, edge_weight_multiplier = 5):
    '''
    edge features oszlopai: origin, destination, flow migration
    node features oszlopai: stock migration
    '''
    mig_net = net.Network(height='320px', width='100%', bgcolor='white', font_color='black', notebook=True)
    # set the physics layout of the network
    mig_net.barnes_hut()
    #Add nodes
    nodes,edges=generate_data(node_features,edge_features, node_size_multiplier, edge_weight_multiplier)
    
    for i, r in nodes.iterrows():
        if logarithm:
            mig_net.add_node(i, i, title=i, size=r["display_nodesize"])
        else:
            mig_net.add_node(i, i, title=i, size=r["stock_migration"])
    #Add edges
    for i, r in edges.iterrows():
        if logarithm:
            mig_net.add_edge(r["origin"], r["destination"], width=r["display_edgesize"])
        else:
            mig_net.add_edge(r["origin"], r["destination"], width=r["migration"])
    return mig_net

def barchart_migracio(state, edge_features, stock=True, origin=True):

    if origin:
        x_column = 'Destination'
        labels = {
                    "Stock": "Kivándorlás (stock)",
                    "Destination": "Befogadó országok",
                }
        title = f"Top 10 befogadó ország. Anyaország: {state}"
    else:
        x_column = 'Origin'
        labels = {
                    "Stock": "Bevándorlás (stock)",
                    "Origin": "Küldő országok",
                }
        title = f"Top 10 küldő ország. Befogadó ország: {state}"
        
    
    
    fig = px.bar(
                edge_features.sort_values('Stock', ascending = False).head(10),
                x=x_column,
                y="Stock",
                labels=labels,
                height=400,
                title=title,
            )
    
    return fig
    
    
    
 #  
 #  if stock:
 #      if origin:
 #          state_table = edge.loc[edge["origin"] == state].nlargest(
 #              min(len(edge.loc[edge["origin"] == state]), 10),
 #              "stock_migration",
 #          )
 #          fig = px.bar(
 #              state_table,
 #              x="destination",
 #              y="stock_migration",
 #              labels={
 #                  "stock_migration": "Kivándorlás (stock)",
 #                  "destination": "Befogadó országok",
 #              },
 #              height=400,
 #              title=f"Top 10 befogadó ország. Anyaország: {state}",
 #          )
 #
 #      else:
 #          state_table = edge.loc[
 #              edge["destination"] == state
 #          ].nlargest(
 #              min(len(edge.loc[edge["destination"] == state]), 10),
 #              "stock_migration",
 #          )
 #          fig = px.bar(
 #              state_table,
 #              x="origin",
 #              y="stock_migration",
 #              labels={
 #                  "stock_migration": "Bevándorlás (stock)",
 #                  "origin": "Anyaországok",
 #              },
 #              height=400,
 #              title=f"Top 10 anyaország. Befogadó ország: {state}",
 #          )
 #  else:
 #      if origin:
 #          state_table = edge.loc[edge["origin"] == state].nlargest(
 #              min(len(edge.loc[edge["origin"] == state]), 10),
 #              "migration",
 #          )
 #          fig = px.bar(
 #              state_table,
 #              x="destination",
 #              y="migration",
 #              labels={
 #                  "migration": "Kivándorlás (flow)",
 #                  "destination": "Befogadó országok",
 #              },
 #              height=400,
 #              title=f"Top 10 befogadó ország. Anyaország: {state}",
 #          )
 #
 #      else:
 #          state_table = edge.loc[
 #              edge["destination"] == state
 #          ].nlargest(
 #              min(len(edge.loc[edge["destination"] == state]), 10),
 #              "migration",
 #          )
 #          fig = px.bar(
 #              state_table,
 #              x="origin",
 #              y="migration",
 #              labels={"migration": "Bevándorlás (flow)", "origin": "Anyaországok"},
 #              height=400,
 #              title=f"Top 10 anyaország. Befogadó ország: {state}",
 #          )
 #
 #  return fig