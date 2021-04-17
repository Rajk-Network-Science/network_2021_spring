# -*- coding: utf-8 -*-

# Run this app with `python migracio_app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import plotly.express as px
from jupyter_dash import JupyterDash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import pprint

DATAPATH = 'C:/Users/HP/Documents/02_CODING/KURZUS_Network/DATA/Kurzushetvege/'

external_stylesheets = [dbc.themes.BOOTSTRAP]

# App meghívása
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# FORMA
colors = {
    'bg' : '#a8dadc'
}

udvozlo_szoveg = '''
        De jó, hogy a dashboardunkra tévedtél! Próbáld ki, mielőtt _migráncsoznál_ egy jót!
        A grafikonokon a World Bank migrációs adatbázisának adatai láthatók.
        Erről ezeket érdemes tudni:
        - bla
        - bliblu
        - bluble
        
        [Adatok leírása](https://datacatalog.worldbank.org/dataset/global-bilateral-migration-database)
        
        [Adatok forrása](https://www.worldbank.org/en/topic/migrationremittancesdiasporaissues/brief/migration-remittances-data)
        
        Az alábbi gombok megnyomásával megnézhetsz néhány érdekes sztorit!
        '''

# DATA
edges = pd.read_csv(DATAPATH + 'edge_list_final.csv')
nodes = pd.read_csv(DATAPATH + 'attributes.csv')
all_from = edges.Origin.unique()
all_to = edges.Destination.unique()
all_year = edges.Year.unique()

# Függvények

# Mendöl térkép készítője
from mapping import map_creation
# Gyenes gráf készítője
from gyenes_vizu import generate_data, graf_vizu



# LAYOUT

app.layout = html.Div(children=[
    html.H1(children='Migráció app', style = {'backgroundColor' : colors['bg']}),
    html.H4(children='Rajk Network Science kurzushétvége, 2021.04.16-18.', style = {'backgroundColor' : colors['bg']}),
    
    dbc.Row(
            [
            dbc.Col(
                [
                    html.Div('Migráció a világban', style = {'textAlign' : 'left', 'fontSize' : 20, 'fontWeight' : 'bold'}),
                    html.Div('Egy adott év kiválasztásával megtekinthető az évben országok közötti áramlás', style = {'textAlign' : 'left'}),
                    
                    # Mendöl térképe
                    dcc.Graph(id = 'terkep_viz'),
                    
                    dcc.Slider(
                        id = 'year_slider_1',
                        min = all_year.min(),
                        max = all_year.max(),
                        value = all_year.max(),
                        marks = {str(year): str(year) for year in all_year},
                        step = None)
                    
                    
                ], style = {'backgroundColor' : colors['bg']}, width = {'size' : 6}
                ),
            
            dbc.Col(
                [
                    html.Div('Migrációs hálózat', style = {'textAlign' : 'left', 'fontSize' : 20, 'fontWeight' : 'bold'}),
                    html.Div('Országok és év kiválasztásával megtekinthető az adott országok adott éves migrációs hálózata', style = {'textAlign' : 'left'}),
                  
                    # Gyenes gráfja
                    html.Iframe(id = 'graf_viz', width = '100%', height = '75%'),
                    
                    dcc.Slider(
                        id = 'year_slider_2',
                        min = all_year.min(),
                        max = all_year.max(),
                        value = all_year.max(),
                        marks = {str(year): str(year) for year in all_year},
                        step = None),
                    dcc.Dropdown(
                        id = 'orszag_dropdown_2', # this number means that this is the 2nd cell on the dashboard (not that this is the 2nd dropdown filter)
                        options = [{'label': i, 'value': i} for i in all_from],
                        value = ['Germany', 'Greece', 'Austria', 'Hungary', 'Turkey'],
                        multi=True
                        )
                      
                ], style = {'backgroundColor' : colors['bg']}, width = {'size' : 6}),
            
            ]), # Row 1 vége
    
    html.Br(),
            
    dbc.Row(
            [
            
            dbc.Col(
                [
                    html.Div('Adott ország vizsgálata', style = {'textAlign' : 'left', 'fontSize' : 20, 'fontWeight' : 'bold'}),
                    html.Div('Egy adott ország esetében megtekinthetők a leggyakoribb küldő vagy fogadó országok', style = {'textAlign' : 'left'}),
                    html.Img(src = 'https://www.amcharts.com/wp-content/uploads/2018/01/horizontal-bar-chart.png',
                             height = 300, width = 384),
                    dcc.Dropdown(
                        id = 'orszag_dropdown_3', # this number means that this is the 3rd cell on the dashboard (not that this is the 3rd dropdown filter)
                        options = [{'label': i, 'value': i} for i in all_from],
                        value = 'Germany'
                        ),
                    dcc.RadioItems(
                        id = 'kibe_radio_3',
                        options = [{'label': 'Beáramlás', 'value' : 'be'},
                                   {'label': 'Kiáramlás', 'value' : 'ki'}], # Itt még át kell írni a value-kat!
                        value = 'be',
                        labelStyle = {'display': 'inline-block'}
                    ),
                ],
                style = {'backgroundColor' : colors['bg']}, width = {'size' : 6}),
            
            dbc.Col(
                [
                    html.Div('Útmutató', style = {'textAlign' : 'left', 'fontSize' : 20, 'fontWeight' : 'bold'}),
                    dcc.Markdown(udvozlo_szoveg),
                ],
                style = {'backgroundColor' : colors['bg']}, width = {'size' : 6}),
                
            ]) # Row 2 vége
    ]) # Layout vége
    
    
# Callbacks

# TÉRKÉP (bal felső)
@app.callback(
    Output('terkep_viz', 'figure'),
    Input('year_slider_1', 'value'))
def update_map(year):
    szurt_nodes = nodes[nodes.Year == year]
    szurt_edges = edges[edges.Year == year]
    fig = map_creation(edgelist_df = szurt_edges, node_df = szurt_nodes, edgeweight_multiplier = 0.02)
    fig.update_layout(transition_duration = 500)
    return fig

# GRÁF (jobb felső)
@app.callback(
    Output('graf_viz', 'srcDoc'),
    Input('year_slider_2', 'value'),
    Input('orszag_dropdown_2', 'value'))
def update_graf(year, orszagok):
    szurt_nodes = nodes[(nodes.Year == year) & (nodes.Origin.isin(orszagok))]
    szurt_edges = edges[(edges.Year == year) & (edges.Origin.isin(orszagok)) & (edges.Destination.isin(orszagok))]
    #generalt_nodes, generalt_edges = generate_data(node_features = szurt_nodes, edge_features = szurt_edges)
    #fig_html = graf_vizu(node_features = generalt_nodes, edge_features = generalt_edges).html
    fig = graf_vizu(node_features = szurt_nodes, edge_features = szurt_edges, edge_weight_multiplier = 5)
    fig.save_graph('gyenes_graf.html')
    return fig.html # open('gyenes_graf.html', 'r').read()


if __name__ == '__main__':
    app.run_server(debug=True)