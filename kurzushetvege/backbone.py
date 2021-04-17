import networkx as nx
import numpy as np
import pandas as pd

def backbone_extraction(G, alpha, directed=True, print_info=True):

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
                    rel_weight=lambda df: df["weight"].pipe(lambda s: s / s.sum())
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
            )["weight"].to_dict()
            if len(edges) > 1
            else {edge[1 - i]: edge[2]["weight"] for edge in edges}
            for i, edges in enumerate(edges_list)
        ]

        for i, edges in enumerate(significant_edges):

            if edges:

                N.add_edges_from(
                    [
                        (n, k, {"weight": v}) if (i == 0) else (k, n, {"weight": v})
                        for k, v in edges.items()
                    ]
                )

    if print_info:
        print(nx.info(N))

    return N

