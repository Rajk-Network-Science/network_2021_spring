#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import pandas as pd
import networkx as nx
import numpy as np
import re
import matplotlib.pyplot as plt
from nxviz import ArcPlot


# In[2]:


COLORNODE = '#40a6d1'
COLOREDGE = '#5be732'


# In[3]:


header = [
    "user_id",
    "public",
    "completion_percentage",
    "gender",
    "region",
    "last_login",
    "registration",
    "AGE",
    "body",
    "I_am_working_in_field",
    "spoken_languages",
    "hobbies",
    "I_most_enjoy_good_food",
    "pets",
    "body_type",
    "my_eyesight",
    "eye_color",
    "hair_color",
    "hair_type",
    "completed_level_of_education",
    "favourite_color",
    "relation_to_smoking",
    "relation_to_alcohol",
    "sign_in_zodiac",
    "on_pokec_i_am_looking_for",
    "love_is_for_me",
    "relation_to_casual_sex",
    "my_partner_should_be",
    "marital_status",
    "children",
    "relation_to_children",
    "I_like_movies",
    "I_like_watching_movie",
    "I_like_music",
    "I_mostly_like_listening_to_music",
    "the_idea_of_good_evening",
    "I_like_specialties_from_kitchen",
    "fun",
    "I_am_going_to_concerts",
    "my_active_sports",
    "my_passive_sports",
    "profession",
    "I_like_books",
    "life_style",
    "music",
    "cars",
    "politics",
    "relationships",
    "art_culture",
    "hobbies_interests",
    "science_technologies",
    "computers_internet",
    "education",
    "sport",
    "movies",
    "travelling",
    "health",
    "companies_brands",
    "more",
    "more"]


# Clearing Nodes

# In[4]:


def nodes():
    df_nodes = pd.read_csv('soc-pokec-profiles.txt', sep='\t', quotechar='"')
    df_nodes.columns = header

    df_nodes = df_nodes[df_nodes.region == 'trenciansky kraj, partizanske']
    
    return df_nodes

def nodes_clearing(df_nodes):
    
    df_nodes_cleared = pd.DataFrame()
    df_nodes_cleared['user_id'] = df_nodes['user_id']
    df_nodes_cleared['gender'] = df_nodes['gender']
    df_nodes_cleared['age'] = df_nodes['AGE']
    
    return df_nodes_cleared



# Select Edges

# In[10]:


def select_edges(df_nodes):
    
    df_edges = pd.read_csv('soc-pokec-relationships.txt', header=None, sep='\t', quotechar='"')

    header = ['start', 'end']
    df_edges.columns = header

    a = df_edges['start'].isin(df_nodes['user_id'])
    b = df_edges['end'].isin(df_nodes['user_id'])

    res1 = [i for i, val in enumerate(list(a)) if val]
    res2 = [i for i, val in enumerate(list(b)) if val]

    c = set(res1).intersection(res2)

    df_edges_cleared = df_edges.iloc[list(c)]
    return df_edges_cleared


# In[16]:


def merge(df_nodes_cleared, df_edges_cleared):
    nagydf = pd.merge(df_edges_cleared,df_nodes_cleared, left_on='start', right_on='user_id', suffixes=('0', '1'))
    nagydf = pd.merge(nagydf,df_nodes_cleared, left_on='end', right_on='user_id', suffixes=('1', '2'))

    edgelist = []
    for i in range(len(nagydf)):
        kislista = []
        kislista.append(nagydf['user_id1'][i])
        kislista.append(nagydf['end'][i])
        edgelist.append(kislista)

    nagydf['edgelist'] = edgelist
    
    return nagydf


# Hálózat létrehozása

# In[18]:


def network_generation(df_nodes_cleared, nagydf):
    G = nx.MultiGraph()
    G.add_nodes_from(df_nodes_cleared['user_id'])
    G.add_edges_from(nagydf['edgelist'])

    nx.draw_shell(G, alpha = .01, edge_color = COLOREDGE, node_color = COLORNODE, node_size=20)


# Elemzés

# In[154]:


def elemzes(nagydf):
    
    pred0=nagydf.groupby("start")[["gender1","gender2" ]].mean().reset_index()
    pred0["predict"]=pred0["gender2"].apply(lambda half: 1 if half<0.5 else 0)

    pred0['is_correct'] = pred0['gender1'] == pred0['predict']
    r = pred0['is_correct'].value_counts()
    print('Az egész mintán nézve:')
    print(r)
    # :(

    lista0 = []
    lista0_20 = []
    lista20_30 = []
    lista30_40 = []
    lista40_50 = []
    lista50_60 = []
    lista60_ = []



    for count, i in enumerate (list(nagydf['age1'])):
        if i == 0:
            lista0.append(count)
        elif i > 0 and i <= 20:
            lista0_20.append(count)
        elif i > 20 and i <= 30:
            lista20_30.append(count)
        elif i > 30 and i <= 40:
            lista30_40.append(count)
        elif i > 40 and i <= 50:
            lista40_50.append(count)
        elif i > 50 and i <= 60:
            lista50_60.append(count)
        elif i > 60:
            lista60_.append(count)

    #print(len(lista0))
    #print(len(lista0_20))
    #print(len(lista20_30))
    #print(len(lista30_40))
    #print(len(lista40_50))
    #print(len(lista50_60))
    #print(len(lista60_))

    df0 = nagydf.iloc[lista0]
    df0_20 = nagydf.iloc[lista0_20]
    df20_30 = nagydf.iloc[lista20_30]
    df30_40 = nagydf.iloc[lista30_40]
    df40_50 = nagydf.iloc[lista40_50]
    df50_60 = nagydf.iloc[lista50_60]
    df60_ = nagydf.iloc[lista60_]


    pred=df0.groupby("start")[["gender1","gender2" ]].mean().reset_index()
    pred["predict"]=pred["gender2"].apply(lambda half: 1 if half<0.5 else 0)

    pred['is_correct'] = pred['gender1'] == pred['predict']
    r = pred['is_correct'].value_counts()
    print('Nincs megadva kor:')
    print(r)
    # :(

    pred=df0_20.groupby("start")[["gender1","gender2" ]].mean().reset_index()
    pred["predict"]=pred["gender2"].apply(lambda half: 1 if half<0.5 else 0)

    pred['is_correct'] = pred['gender1'] == pred['predict']
    r = pred['is_correct'].value_counts()
    print('20 év alatt:')

    print(r)
    # :(

    pred=df20_30.groupby("start")[["gender1","gender2" ]].mean().reset_index()
    pred["predict"]=pred["gender2"].apply(lambda half: 1 if half<0.5 else 0)

    pred['is_correct'] = pred['gender1'] == pred['predict']
    r = pred['is_correct'].value_counts()
    print('20 és 30 év között:')
    print(r)
    # :(

    pred=df30_40.groupby("start")[["gender1","gender2" ]].mean().reset_index()
    pred["predict"]=pred["gender2"].apply(lambda half: 1 if half<0.5 else 0)

    pred['is_correct'] = pred['gender1'] == pred['predict']
    r = pred['is_correct'].value_counts()
    print('30 és 40 év között:')
    print(r)
    # :|

    pred=df40_50.groupby("start")[["gender1","gender2" ]].mean().reset_index()
    pred["predict"]=pred["gender2"].apply(lambda half: 1 if half<0.5 else 0)

    pred['is_correct'] = pred['gender1'] == pred['predict']

    r = pred['is_correct'].value_counts()
    print('40 és 50 év között:')

    print(r)
    # :|

    pred=df50_60.groupby("start")[["gender1","gender2" ]].mean().reset_index()
    pred["predict"]=pred["gender2"].apply(lambda half: 1 if half<0.5 else 0)

    pred['is_correct'] = pred['gender1'] == pred['predict']
    r = pred['is_correct'].value_counts()
    print('50 és 60 év között:')
    print(r)
    # :|

    pred=df60_.groupby("start")[["gender1","gender2" ]].mean().reset_index()
    pred["predict"]=pred["gender2"].apply(lambda half: 1 if half<0.5 else 0)

    pred['is_correct'] = pred['gender1'] == pred['predict']
    r = pred['is_correct'].value_counts()
    print('60 év felett:')
    print(r)
    # :(


# Kor szerinti csoportosítás

# In[57]:


def by_age(nagydf):
    
    pred=nagydf.groupby(['age1', "gender1"])[["gender2" ]].mean().reset_index()
    pred["predict"]=pred["gender2"].apply(lambda half: 1 if half<0.5 else 0)
    pred['is_correct'] = pred['gender1'] == pred['predict']
    pred.head(50)


    #r = pred['is_correct'].value_counts()
    #r

    pred10=nagydf.groupby("start")
    pred10.first()

    pred=pred10[["gender1","gender2" ]].mean().reset_index()
    pred["predict"]=pred["gender2"].apply(lambda half: 1 if half<0.5 else 0)

    pred['is_correct'] = pred['gender1'] == pred['predict']
    age_k = pred10.first()['age1']
    pred['startage'] = list(age_k)
    pred

    agedf = pd.DataFrame()
    agedf['age'] = list(set(list(age_k)))
    agedf['count'] = np.nan
    agedf

    for count, i in enumerate(agedf['age']):
        minilista = []
        for k in range(len(pred)):
            if i == pred['startage'][k]:
                minilista.append(pred['is_correct'][k])
            try:
                agedf['count'][count] = minilista.count(True)/len(minilista)
            except:
                pass

    agedf.plot(title = 'Az előrejelzés sikeressége a megfigyelt csomópontok kora szerint', x="age", y="count")

