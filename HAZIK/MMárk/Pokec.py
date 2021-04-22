#!/usr/bin/env python
# coding: utf-8

# In[136]:


import csv
import pandas as pd
import networkx as nx
import numpy as np
import re
import matplotlib.pyplot as plt


# In[137]:


COLORNODE = '#40a6d1'
COLOREDGE = '#5be732'


# In[139]:


def nodelist():
    lines = []
    nodes = []
    
    with open('soc-pokec-profiles.txt', encoding="Latin-1") as f:
        for line in f:
            if 'trenciansky kraj, partizanske' in line:
                lines.append(line)

    for i in lines:
        #dic = {
            #'UserID': (re.search('([^\t]*)', i).group(1))
            #'Age': (re.search('\t([^\]*)', i).group(0)),
            #'Gender': (re.search('\t([^\]*)', i).group(1)),
            #'Last_Login_Days': (re.search('\t([^\]*)', i).group(2)),
            #'Registration_Days': (re.search('\t([^\]*)', i).group(4)),
            #'User_ID': (re.search('\t([^\]*)', i).group(5))}

        nodes.append(int((re.search('([^\t]*)', i).group(1))))
    len(nodes)
    nodeset = set(nodes)


# In[141]:


nodelist()


# In[140]:


def edgelist():
    
    edgelist = []

    edgelist_process = lambda x: [int(num) for num in x.split('\t')]

    with open('soc-pokec-relationships.txt') as e:
        for line in e:
            edgelist.append(edgelist_process(line))

    len(edgelist)


# In[142]:


edgelist()


# In[7]:


def edge_selection():
    
    elso = []
    masodik = []

    for i in edgelist:
        elso.append(i[0])
        masodik.append(i[1])

    s1 = pd.Series(elso)
    df1 = pd.DataFrame(s.isin(nodes))

    s2 = pd.Series(masodik)
    df2 = pd.DataFrame(s2.isin(nodes))

    a = s1.isin(nodeset)
    b = s2.isin(nodeset)


    res1 = [i for i, val in enumerate(list(a)) if val]
    res2 = [i for i, val in enumerate(list(b)) if val]

    c = set(res1).intersection(res2)

    vegsolista = []
    for i in list(c):
        vegsolista.append(edgelist[i])


# In[ ]:


edge_selection()


# In[ ]:


def graph_creation():

    G = nx.MultiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(vegsolista)
    nx.info(G)
    nx.draw(G, alpha = .3, edge_color = COLOREDGE, node_color = COLORNODE, node_size=20)

    print('Csúcsok száma:', G.number_of_nodes())
    #print('Klaszterezettségi együttható:', nx.average_clustering(G))
    degrees = [len(list(G.neighbors(n))) for n in G.nodes()]
    print('Átlagos fokszám:', sum(degrees)/len(degrees))

    fig, ax = plt.subplots()
    ax.hist(degrees, bins = 20, log = True)
    ax.set_xlabel('Kapcsolatok száma')
    ax.set_ylabel('Elemek száma')
    ax.set_title(r'Fokszámeloszlás')


