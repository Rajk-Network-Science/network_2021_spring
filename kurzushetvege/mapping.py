import plotly.graph_objects as go
import pandas as pd

def map_creation(edgelist_df, node_df, edgecolor="red", cutoff_edgeweight = 1000, edgeweight_multiplier = 0.02, node_size_multiplier = 5):
    
    fig = go.Figure()
    edgelist_df_selected = edgelist_df.loc[edgelist_df['Flow'] > cutoff_edgeweight,:].copy(deep=True)
    edgelist_df_selected['edgeweight'] = edgelist_df['Flow']/edgelist_df['Flow'].mean()*edgeweight_multiplier
    node_df['weighted_stock'] = node_df['Stock']/node_df['Stock'].mean() * node_size_multiplier

    if len(edgelist_df_selected) > 5000:
        edgelist_df_selected = edgelist_df_selected.head(5000)
        
    fig.add_trace(go.Scattergeo(
    locationmode = 'ISO-3',
    lon = node_df['Origin_longitude'],
    lat = node_df['Origin_latitude'],
    hoverinfo = 'text',
    text = node_df['Origin'],
    mode = 'markers',
    marker = dict(
        size = node_df['weighted_stock'],
        color = 'rgb(255, 0, 0)',
        line = dict(
            width = 3,
            color = 'rgb(68, 68, 68, 0)'
        )
    )))
    
    for index, row in edgelist_df_selected.iterrows():
        fig.add_trace(
            go.Scattergeo(
                locationmode = 'ISO-3',
                lon = [row['Origin_longitude'], row['Destination_longitude']],
                lat = [row['Origin_latitude'], row['Destination_latitude']],
                mode = 'lines',
                line = dict(width = row['edgeweight'], color = edgecolor),
            ))
    fig.update_layout(
        width = 800,
        height= 400,
        showlegend = False,
          margin=go.layout.Margin(
                    l=0, #left margin
                    r=0, #right margin
                    b=0, #bottom margin
                    t=0  #top margin
    ),
        geo = dict(
            scope = 'world',
            projection_type = 'azimuthal equal area',
            showcountries = True,
            landcolor = 'LightGreen',
            showocean = True,
            oceancolor = 'LightBlue',
            countrycolor = 'Black'
        ))
    return fig