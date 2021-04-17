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
import os


DATAPATH = 'DATA/'

external_stylesheets = [dbc.themes.BOOTSTRAP]

# App meghívása
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# FORMA
colors = {
    'bg' : 'white'
}

udvozlo_szoveg = '''
        De jó, hogy a dashboardunkra tévedtél! Próbáld ki, mielőtt _migráncsoznál_ egy jót!
        A grafikonokon a World Bank migrációs adatbázisának adatai láthatók.
        
        Az app az 1960–2010 közötti, illetve 2013 és 2017 évi időszakok migrációs folyamatait
        szemlélteti a World Bank kétoldalú migrációs mátrixai alapján. Így egy átfogó kép adódik az elmúlt 7 évtized kétoldalú globális migrációjáról. 

        Az app 1. vizualizációja a kiválasztott időszakra mutatja a globális migráció alakulását a világtérképen.

        Az app 2. vizualizációja adott évre a kiválasztott országok migrációs gráfját mutatja be,
        ahol az ország csúcsok kövérségét a migráns állomány határozza meg, az országok közötti élek vastagságát pedig az állományváltozás.

        Az app 3. vizualizációja a kiválasztott ország(ok) ki- vagy bevándorlók állományát, vagy ennek az
        előző időszakhoz képesti változását mutatja a 10 legfontosabb befogadó- vagy célország körében.
        
        [Adatok forrása](https://www.worldbank.org/en/topic/migrationremittancesdiasporaissues/brief/migration-remittances-data)
        
        Az alábbi gomb megnyomásával megnézhetsz egy érdekes sztorit!
        '''
        
burdzs_szoveg = '''
        A sivatagi területen épülő új Arab metropoliszek rengeteg
        dél- és kelet-ázsiai munkást vonzottak az Öböl-országok térségébe.
        Az olaj exportra épülő gazdaságok fejlődéséhez a magasan képzett-jellemzően
        nyugati országokból érkező - munkások mellett az olcsó, szegényebb országokból
        érkező munkaerőre is szükség volt. Remek példa erre a világ legmagasabb
        építményének a Burj-Khalifa felhőkarcolónak története, mely felépítésén 2008-ban
        7500 munkás dolgozott, a Guardian beszámolója alapján átlagosan kevesebb, mint *1200* forintos (£2.9) napi bérért.
    '''        


# DATA
edges = pd.read_csv(os.path.join(DATAPATH, 'edge_list_final.csv'))
nodes = pd.read_csv(os.path.join(DATAPATH , 'attributes.csv'))
all_from = edges.Origin.unique()
all_to = edges.Destination.unique()
all_year = edges.Year.unique()

# Függvények

# Hobot adatelőkészítője
from Hobot.dataprep import masterfilter
from Hobot.country_continent import country_dict
# Mendöl térkép készítője
from mapping import map_creation
# Gyenes gráf és barchart készítője
from gyenes_vizu import generate_data, graf_vizu, barchart_migracio

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
                    html.Div(html.Div(dcc.Graph(id = 'terkep_viz'), style={'width':'100%', 'height' : '400px'}),style={'width':'100%'}),
                    
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
                    html.Iframe(id = 'graf_viz', width = '100%', height = '350px', style={'background':"white"}),
                    
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
                    dcc.Graph(id = 'barchart'),         
                             
                             
                             
                    dcc.Dropdown(
                        id = 'orszag_dropdown_3', # this number means that this is the 3rd cell on the dashboard (not that this is the 3rd dropdown filter)
                        options = [{'label': i, 'value': i} for i in all_from],
                        value = 'Germany'
                        ),
                    dcc.RadioItems(
                        id = 'kibe_radio_3',
                        options = [{'label': 'Beáramlás', 'value' : 'be'},
                                   {'label': 'Kiáramlás', 'value' : 'ki'}],
                        value = 'be',
                        labelStyle = {'display': 'inline-block'}
                    ),
                    dcc.Slider(
                        id = 'year_slider_3',
                        min = all_year.min(),
                        max = all_year.max(),
                        value = all_year.max(),
                        marks = {str(year): str(year) for year in all_year},
                        step = None),
                ],
                style = {'backgroundColor' : colors['bg']}, width = {'size' : 6}),
            
            dbc.Col(
                [
                    html.Div('Útmutató', id = 'utmutato_title', style = {'textAlign' : 'left', 'fontSize' : 20, 'fontWeight' : 'bold'}),
                    dcc.Markdown(udvozlo_szoveg, id = 'leiras'),
                    dcc.RadioItems(
                        id = 'szoveg_valaszto',
                        options = [{'label' : 'Alapállapot', 'value' : 'udv'},
                                   {'label' : 'Burdzs Kalifa sztori', 'value' : 'burdzs'}],
                        value = 'udv',
                        labelStyle = {'display': 'inline-block'},
                        style = {'margin-right' : '10px'}
                    
                    )
                ],
                )
                
            ]) # Row 2 vége
    ]) # Layout vége
    
    
# Callbacks

# TÉRKÉP (bal felső)
@app.callback(
    Output('terkep_viz', 'figure'),
    Input('year_slider_1', 'value'))
def update_map(year):
    szurt_edges, szurt_nodes = masterfilter(edges, 0.04, "Stock", year = [year])
    fig = map_creation(edgelist_df = szurt_edges, node_df = szurt_nodes.reset_index(), edgeweight_multiplier = 0.1, node_size_multiplier = 2)

    fig.update_layout(transition_duration = 500)
    return fig

# GRÁF (jobb felső)
@app.callback(
    Output('graf_viz', 'srcDoc'),
    Input('year_slider_2', 'value'),
    Input('orszag_dropdown_2', 'value'))
def update_graf(year, orszagok):
    szurt_edges, szurt_nodes = masterfilter(edges, 1, "Stock", year = [year], origin = orszagok, destination = orszagok)
    fig = graf_vizu(node_features = szurt_nodes.reset_index(), edge_features = szurt_edges, edge_weight_multiplier = 5)
    fig.save_graph('gyenes_graf.html')
    return fig.html
    
# BARCHART (bal alsó)
@app.callback(
    Output('barchart', 'figure'),
    Input('orszag_dropdown_3', 'value'),
    Input('kibe_radio_3', 'value'),
    Input('year_slider_3', 'value'))
def update_barchart(orszag, kibe, year):
    if kibe == 'be':
        szurt_edges, szurt_nodes = masterfilter(edges, 1, "Stock", year = [year], destination = [orszag])
        fig = barchart_migracio(orszag, szurt_edges, origin = False)
    else:
        szurt_edges, szurt_nodes = masterfilter(edges, 1, "Stock", year = [year], origin = [orszag])
        fig = barchart_migracio(orszag, szurt_edges, origin = True)
    
    return fig
    
# BURDZS GOMB
@app.callback(
    Output('year_slider_1', 'value'),
    Output('year_slider_2', 'value'),
    Output('orszag_dropdown_2', 'value'),
    Output('orszag_dropdown_3', 'value'),
    Output('kibe_radio_3', 'value'),
    Output('year_slider_3', 'value'),
    Output('utmutato_title', 'children'),
    Output('leiras', 'children'),
    Input('szoveg_valaszto', 'value'))
def update_filters(szovegopcio):
    if szovegopcio == 'burdzs':
        return 2010, 2010, ['United Arab Emirates', 'India', 'Bangladesh', 'Pakistan', 'Egypt, Arab Rep.', 'Philippines', 'Indonesia', 'Yemen, Rep.', 'Jordan', 'Sudan', 'Sri Lanka'], 'United Arab Emirates', 'be', 2010, 'Épül a Burdzs Kalifa', burdzs_szoveg
    else:
        return 2017, 2017, ['Germany', 'Greece', 'Austria', 'Hungary', 'Turkey'], 'Germany', 'be', 2017, 'Útmutató', udvozlo_szoveg
        


if __name__ == '__main__':
    app.run_server(debug=True)