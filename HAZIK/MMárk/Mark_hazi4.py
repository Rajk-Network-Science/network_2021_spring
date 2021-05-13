#!/usr/bin/env python
# coding: utf-8

# Csomagok importálása

# In[89]:


import matplotlib
import networkx as nx
import csv
import matplotlib.pyplot as plt
import statistics
import numpy as np
import pandas as pd
import random


# In[90]:


COLORNODE = '#40a6d1'
COLOREDGE = '#5be732'


# Kezdeti Erdős-Rényi gráf (N = 30, p = 0,2)

# In[95]:


def erdos_renyi():
    G= nx.erdos_renyi_graph(20,0.2) 
    nx.draw(G, with_labels=True) 
    plt.show()
    nx.draw(G, alpha = .3, edge_color = COLOREDGE, node_color = COLORNODE, node_size=50)


# In[96]:


erdos_renyi()


# Kapcsolatválasztó modell

# In[97]:


def link_selection():

    G= nx.erdos_renyi_graph(20,0.2)
    degrees = []
    normalised = []
    cluster = []
    for i in list(G.nodes):
        degrees.append(G.degree(i))
        
    for i in degrees:
        normalised.append(i/(sum(degrees)))
    
    for i in range(20, 1020):
        nodefix = list(G.nodes)
        G.add_node(i)
        a = random.choices(nodefix, weights=degrees, k=1)
        G.add_edge(a[0], i)
        b = random.choices(nodefix, weights=degrees, k=1)
        G.add_edge(b[0], i)
        c = random.choices(nodefix, weights=degrees, k=1)
        G.add_edge(c[0], i)
        
        degrees = []
        for x in list(G.nodes):
            degrees.append(G.degree(x))
        
        normalised = []
        for y in degrees:
            normalised.append(y/(sum(degrees)))
        
        if i % 10 == 0:
            cluster.append((np.log(i))**2/(i))
        
    print('Csúcsok száma:', G.number_of_nodes())
    print('Klaszterezettségi együttható:', nx.average_clustering(G))
    print('Átlagos fokszám:', sum(degrees)/len(degrees))
    if nx.is_connected(nx.to_undirected(G)):
        print('Átmérő:', nx.algorithms.distance_measures.diameter(G))
        print('Átlagos legrövidebb út:', nx.average_shortest_path_length(G))
    else:
        print('A gráf nem kapcsolódik össze teljesen, vannak izolált pontok, vagyis több komponensből áll. Ezért végtelen az átmérője és nem talál átlagos legrövidebb utat.')
    
    nx.draw(G, alpha = .3, edge_color = COLOREDGE, node_color = COLORNODE, node_size=50)
    
    fig, ax = plt.subplots()
                    
    ax.hist(degrees, bins = 30, log = True)
    ax.set_xlabel('Kapcsolatok száma')
    ax.set_ylabel('Elemek száma')
    ax.set_title(r'Fokszámeloszlás')
    
    fig, ax = plt.subplots()
                    
    ax.hist(cluster, bins = 50, log = True)
    ax.set_xlabel('Csúcsok száma')
    ax.set_ylabel('<C>')
    ax.set_title(r'Klaszterezettségi együttható')


# In[94]:


link_selection()


# Másolómodell

# In[98]:


def copy_modell():

    G2= nx.erdos_renyi_graph(20,0.2)

    cluster2 = []
    p = 0.05
    egy_p = 1-p



    for i in range(20, 1020):
        floaty = random.random()
        G2.add_node(i)
        for g in range(3):
            if floaty < p:
                G2.add_edge(1, i)
            else:
                G2.add_edge(random.choice(list(G2.nodes)), i)

        if i % 10 == 0:
            cluster2.append((np.log(i))**2/(i))    


    nx.draw(G2, alpha = .3, edge_color = COLOREDGE, node_color = COLORNODE, node_size=50)

    degrees2 = []
    for i in list(G2.nodes):
        degrees2.append(G2.degree(i))


    print('Csúcsok száma:', G2.number_of_nodes())
    print('Klaszterezettségi együttható:', nx.average_clustering(G2))
    print('Átlagos fokszám:', sum(degrees2)/len(degrees2))
    if nx.is_connected(nx.to_undirected(G2)):
        print('Átmérő:', nx.algorithms.distance_measures.diameter(G2))
        print('Átlagos legrövidebb út:', nx.average_shortest_path_length(G2))
    else:
        print('A gráf nem kapcsolódik össze teljesen, vannak izolált pontok, vagyis több komponensből áll. Ezért végtelen az átmérője és nem talál átlagos legrövidebb utat.')
        
    fig, ax = plt.subplots()

    ax.hist(degrees2, bins = 30, log = True)
    ax.set_xlabel('Kapcsolatok száma')
    ax.set_ylabel('Elemek száma')
    ax.set_title(r'Fokszámeloszlás')

    fig, ax = plt.subplots()

    ax.hist(cluster2, bins = 50, log = True)
    ax.set_xlabel('Csúcsok száma')
    ax.set_ylabel('<C>')
    ax.set_title(r'Klaszterezettségi együttható')


# In[88]:


copy_modell()


# Barabási-Albert modell

# In[81]:


def B_M():
    
    
    def rand_prob_node():
        nodes_probs = []
        for node in G3.nodes():
            node_degr = G3.degree(node)
            node_proba = node_degr / (2 * len(G3.edges()))
            nodes_probs.append(node_proba)
        random_proba_node = np.random.choice(G3.nodes(),p=nodes_probs)
        return random_proba_node

    def add_edge():
        if len(G3.edges()) == 0:
            random_proba_node = 0
        else:
            random_proba_node = rand_prob_node()
        new_edge = (random_proba_node, new_node)
        if new_edge in G3.edges():
            add_edge()
        else:
            G3.add_edge(new_node, random_proba_node)

    cluster3 = []

    init_nodes = 20
    final_nodes = 1020
    m_parameter = 3

    G3 = nx.complete_graph(init_nodes)

    count = 0
    new_node = init_nodes

    for i in range(final_nodes - init_nodes):
        G3.add_node(init_nodes + count)
        count += 1
        for e in range(0, m_parameter):
            add_edge()
        new_node += 1

        if (i+1) % 10 == 0:
            cluster3.append((np.log(i+1))**2/(i+1))


    degrees3 = []
    for i in list(G3.nodes):
        degrees3.append(G3.degree(i))

    print('Csúcsok száma:', G3.number_of_nodes())
    print('Klaszterezettségi együttható:', nx.average_clustering(G3))
    print('Átlagos fokszám:', sum(degrees3)/len(degrees3))
    if nx.is_connected(nx.to_undirected(G3)):
        print('Átmérő:', nx.algorithms.distance_measures.diameter(G3))
        print('Átlagos legrövidebb út:', nx.average_shortest_path_length(G3))
    else:
        print('A gráf nem kapcsolódik össze teljesen, vannak izolált pontok, vagyis több komponensből áll. Ezért végtelen az átmérője és nem talál átlagos legrövidebb utat.')


    nx.draw(G3, alpha = .3, edge_color = COLOREDGE, node_color = COLORNODE, node_size=50)

    fig, ax = plt.subplots()

    ax.hist(degrees3, bins = 30, log = True)
    ax.set_xlabel('Kapcsolatok száma')
    ax.set_ylabel('Elemek száma')
    ax.set_title(r'Fokszámeloszlás')

    fig, ax = plt.subplots()

    ax.hist(cluster3, bins = 50, log = True)
    ax.set_xlabel('Csúcsok száma')
    ax.set_ylabel('<C>')
    ax.set_title(r'Klaszterezettségi együttható')


# In[82]:


B_M()


# In[ ]:




