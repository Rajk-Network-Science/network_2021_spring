# -*- coding: utf-8 -*-

# Run this app with `python migracio_app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# FORMA
# pl. színek

# DATA
df = pd.DataFrame({
    'koli' : ['rajk', 'szisz', 'evk'],
    'iq' : [150, 130, 110],
    'arc' : [8, 6, 10],
    'color' : ['green', 'black', 'red']
    })

# VIZUÁLOK

fig1 = px.bar(df, x='koli', y='iq', color = 'koli', color_discrete_sequence = df['color'])
fig2 = px.bar(df, x='koli', y='arc', color = 'koli', color_discrete_sequence = df['color'])




app.layout = html.Div(children=[
    html.H1(children='Migráció app'),
    html.H4(children='Rajk Network Science kurzushétvége, 2021.04.16-18.'),
    
    dbc.Row(
        [
        
        dbc.Col(
            [
                html.Div("Bal felső", style = {'textAlign' : 'center', 'fontSize' : 14}),
                html.Div("A szakkolisok IQ-ja", style = {'textAlign' : 'center', 'fontSize' : 20}),
                html.Br(),
                dcc.Graph(
                    id = 'iq_graf',
                    figure = fig1
                    ),
                html.Label('Szűrő próba - MÉG NEM SZŰR'),
                dcc.Dropdown(
                    options=[
                        {'label': 'Rajk', 'value': 'rajk'},
                        {'label': 'SZISZ', 'value': 'szisz'},
                        {'label': 'EVK', 'value': 'evk'}
                    ],
                    value=['rajk', 'szisz'],
                    multi=True
                    )
            ], align = 'center'),
        
        dbc.Col(
            [
                html.Div("Jobb felső", style = {'textAlign' : 'center', 'fontSize' : 14}),
                html.Div("A szakkolisok arca", style = {'textAlign' : 'center', 'fontSize' : 20}),
                dcc.Graph(
                    id = 'arc_graf',
                    figure = fig2
                    )
            ], align = 'center'),
        
        ],
        ),
        
    dbc.Row(
        [
        
        dbc.Col(
            html.Div("Bal alsó", style = {'textAlign' : 'center', 'fontSize' : 14}),
            align = 'center'),
        
        dbc.Col(
            html.Div("Jobb alsó", style = {'textAlign' : 'center', 'fontSize' : 14}),
            align = 'center'),
        
        ],
        ),
    

])


if __name__ == '__main__':
    app.run_server(debug=True)