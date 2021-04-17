import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def filter_edge_list(df, year=None, origin=None, destination=None):
    
    #filtering
    if year:
        df = df.loc[df["Year"].isin(year)]
    if origin:
        df = df.loc[df["Origin"].isin(origin)]
    if destination:
        df = df.loc[df["Destination"].isin(destination)]
        
    return df


def filter_attributes(df, year=None, origin=None, destination=None):
    
    #filtering
    if year:
        df = df.loc[df["Year"].isin(year)]
    if origin:
        df = df.loc[df["Origin"].isin(origin)]
    if destination:
        df = df.loc[df["Destination"].isin(destination)]
    
    #making the aggregates
    attributes=df[["Origin", "Stock", "Year", "Origin_latitude", "Origin_longitude"]]
    stocks=attributes.groupby(["Origin", "Year"])["Stock"].sum()
    attributes=attributes.groupby(["Origin", "Year"])[["Origin_latitude", "Origin_longitude"]].mean()
    attributes["Stock"]=stocks
    
    return attributes


import networkx as nx
import numpy as np
import pandas as pd
import scipy.integrate as integrate

def backbone_extraction(G, alpha, weight, directed=True, print_info=False):


    N = nx.DiGraph() if directed else nx.Graph()

    for n in G.nodes():

        if directed:
            edges_list = [G.out_edges(n, data=True), G.in_edges(n, data=True)]

        else:
            edges_list = [G.edges(n, data=True)]

        significant_edges = [
            (
                pd.DataFrame({edge[1 - i]: edge[2] for edge in edges})
                .T.assign(
                    rel_weight=lambda df: df[weight].pipe(lambda s: s / s.sum())
                )
                .pipe(
                    lambda df: df.assign(
                        alpha=df["rel_weight"].apply(
                            lambda w: (
                                1
                                - (len(edges) - 1)
                                * integrate.quad(
                                    lambda x: (1 - x) ** (len(edges) - 2), 0, w
                                )[0]
                            )
                        )
                    )
                )
                .loc[lambda df: df["alpha"] < alpha]
            )[weight].to_dict()
            if len(edges) > 1
            else {edge[1 - i]: edge[2][weight] for edge in edges}
            for i, edges in enumerate(edges_list)
        ]

        for i, edges in enumerate(significant_edges):

            if edges:

                N.add_edges_from(
                    [
                        (n, k, {weight: v}) if (i == 0) else (k, n, {weight: v})
                        for k, v in edges.items()
                    ]
                )

    if print_info:
        print(nx.info(N))

    return N 

def grapth_to_edge_list(G, df, weight):
    edge_attr = nx.to_pandas_edgelist(G)
    edge_attr = edge_attr.merge(df, how="left", left_on=["source", "target", weight], right_on=["Origin", "Destination", weight])
    edge_attr = edge_attr[["Origin", "Destination", "Year", "Stock", "Flow", "Origin_latitude", "Origin_longitude", "Destination_latitude", "Destination_longitude"]]
    return edge_attr

def masterfilter(df, alpha, weight, year=None, origin=None, destination=None):

    # making edgelist and node attribute dataframes
    edge_list = filter_edge_list(df, year, origin, destination)

    # making a graph
    G = nx.from_pandas_edgelist(
        edge_list,
        "Origin",
        "Destination",
        df.columns.tolist()[2:],
        create_using=nx.DiGraph(),
    )

    # making the backbone of the story
    G = backbone_extraction(G, alpha, weight, directed=True, print_info=False)
    edge_list = grapth_to_edge_list(G, df, weight)
    attributes = filter_attributes(
        df,
        year=year,
        destination=destination,
        origin=edge_list.Origin.unique().tolist(),
    )
   
    if year:
        edge_list=edge_list.loc[edge_list["Year"].isin(year)]

    return edge_list, attributes