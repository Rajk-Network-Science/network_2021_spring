#!/usr/bin/env python
# coding: utf-8

# In[3]:


import plotly.graph_objects as go
import pandas as pd


# In[5]:


year = 1970
df_coordinates = pd.read_csv('edge_list_final.csv')
df_coordinates_selected = df_coordinates[df_coordinates['Year'] == year]

df_nodes = pd.read_csv('attributes.csv')
df_nodes_selected = df_nodes[df_nodes['Year'] == year]


# In[7]:


def map_creation(edgelist_df, node_df, edgecolor, cutoff_edgeweight, edgeweight_multiplier = 1):
    
    fig = go.Figure()
    edgelist_df_selected = edgelist_df[edgelist_df['Flow'] > cutoff_edgeweight]
    edgelist_df_selected['edgeweight'] = edgelist_df['Flow']/edgelist_df['Flow'].mean()*edgeweight_multiplier
    
    if len(edgelist_df_selected) > 1000:
        print('A hálózat több, mint 1000 élt tartalmaz, a számítási kapacitások korlátossága miatt, csak a felső 1000 kerül ábrázolásra.')
        edgelist_df_selected = edgelist_df_selected.head(1000)
        
    fig.add_trace(go.Scattergeo(
    locationmode = 'ISO-3',
    lon = node_df['Origin_longitude'],
    lat = node_df['Origin_latitude'],
    hoverinfo = 'text',
    text = df_coordinates['Origin'],
    mode = 'markers',
    marker = dict(
        size = 2,
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
                #opacity = float(row['1960 [1960]']) / float(df_selected['1960 [1960]'].max()),
            ))
    fig.update_layout(
        title_text = 'Országok közötti migráció',
        showlegend = True,
        geo = dict(
            scope = 'world',
            projection_type = 'azimuthal equal area',
            showcountries = True,
            landcolor = 'rgb(218, 212, 131)',
            countrycolor = 'Black'
        ))
    return fig


# In[8]:


map_creation(df_coordinates_selected, df_nodes_selected, 'red', 1000, 0.02)

