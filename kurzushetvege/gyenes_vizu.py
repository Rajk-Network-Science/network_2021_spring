import pandas as pd
import numpy as np
import itertools
import networkx as nx
from pyvis import network as net
from IPython.core.display import display, HTML
import plotly.express as px

#node_features=pd.read_csv("attributes.csv")
#edge_features=pd.read_csv("edge_list_final.csv")


def generate_data(node_features,edge_features):
    '''
    data: node attributes
    data2: edge list
    '''
    node_features.columns=['Origin','Year','Origin_latitude','Origin_longitude','stock_migration']
    #node_features=node_features.loc[node_features['Year'] == 2017]
    node_features = node_features.set_index("Origin")
    node_features=node_features.drop(['Year','Origin_latitude','Origin_longitude'], axis=1)
    
    #edge_features=edge_features.loc[edge_features['Year'] == 2017]
    edge_features=edge_features.drop(['Year','Origin_latitude','Origin_longitude', 'Destination_latitude','Destination_longitude'], axis=1)
    edge_features.columns=['origin','destination','stock_migration','migration']
    
    node_features["display_nodesize"] = (
        node_features["stock_migration"]
        .pipe(lambda s: np.log(s.apply(lambda x: max(1,x))))
        .pipe(lambda s: s / np.nanmean(s) * 100)
    )
    edge_features["display_edgesize"] = (
        edge_features["migration"]
        .pipe(lambda s: s / np.nanmax(s))
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
    return {"node_features": node_features, "edge_features": edge_features}

def graf_vizu(edge_features,node_features, logarithm=True):
    '''
    edge features oszlopai: origin, destination, flow migration
    node features oszlopai: stock migration
    '''
    mig_net = net.Network(height='750px', width='100%', bgcolor='#222222', font_color='white', notebook=True)
    # set the physics layout of the network
    mig_net.barnes_hut()
    #Add nodes
    features = generate_data(node_features, edge_features)
    
    for i, r in features["node_features"].iterrows():
        if logarithm:
            mig_net.add_node(i, label=i, title=i, size=r["display_nodesize"], shape="circle", labelHighlightBold=True)
        else:
            mig_net.add_node(i, label=i, title=i, size=r["stock_migration"], shape="circle", labelHighlightBold=True)
    #Add edges
    for i, r in features["edge_features"].iterrows():
        if logarithm:
            mig_net.add_edge(r["origin"], r["destination"], width=r["display_edgesize"])
        else:
            mig_net.add_edge(r["origin"], r["destination"], width=r["migration"])
    return mig_net

def barchart(state, stock=True, origin=True):
    features = generate_data(node_features, edge_features)
    if stock:
        if origin:
            state_table = features["edge_features"].loc[features["edge_features"]["origin"] == state].nlargest(
                min(len(features["edge_features"].loc[features["edge_features"]["origin"] == state]), 10),
                "stock_migration",
            )
            fig = px.bar(
                state_table,
                x="destination",
                y="stock_migration",
                labels={
                    "stock_migration": "Kivándorlás (stock)",
                    "destination": "Befogadó országok",
                },
                height=400,
                title=f"Top 10 befogadó ország. Anyaország: {state}",
            )

        else:
            state_table = features["edge_features"].loc[
                features["edge_features"]["destination"] == state
            ].nlargest(
                min(len(features["edge_features"].loc[features["edge_features"]["destination"] == state]), 10),
                "stock_migration",
            )
            fig = px.bar(
                state_table,
                x="origin",
                y="stock_migration",
                labels={
                    "stock_migration": "Bevándorlás (stock)",
                    "origin": "Anyaországok",
                },
                height=400,
                title=f"Top 10 anyaország. Befogadó ország: {state}",
            )
    else:
        if origin:
            state_table = features["edge_features"].loc[features["edge_features"]["origin"] == state].nlargest(
                min(len(features["edge_features"].loc[features["edge_features"]["origin"] == state]), 10),
                "migration",
            )
            fig = px.bar(
                state_table,
                x="destination",
                y="migration",
                labels={
                    "migration": "Kivándorlás (flow)",
                    "destination": "Befogadó országok",
                },
                height=400,
                title=f"Top 10 befogadó ország. Anyaország: {state}",
            )

        else:
            state_table = features["edge_features"].loc[
                features["edge_features"]["destination"] == state
            ].nlargest(
                min(len(features["edge_features"].loc[features["edge_features"]["destination"] == state]), 10),
                "migration",
            )
            fig = px.bar(
                state_table,
                x="origin",
                y="migration",
                labels={"migration": "Bevándorlás (flow)", "origin": "Anyaországok"},
                height=400,
                title=f"Top 10 anyaország. Befogadó ország: {state}",
            )

    return fig