#!/usr/bin/env python
# coding: utf-8

# In[27]:


import matplotlib
import networkx as nx
import urllib
import csv
import matplotlib.pyplot as plt
import statistics
import numpy as np


# In[68]:


def generate_hazi3():
        g = nx.read_edgelist("CA-GrQc.txt",create_using=nx.DiGraph(), nodetype = int)

        print('Csúcsok száma:', g.number_of_nodes())
        print('Klaszterezettségi együttható:', nx.average_clustering(g))
        degrees = [len(list(g.neighbors(n))) for n in g.nodes()]
        print('Átlagos fokszám:', sum(degrees)/len(degrees))
        if nx.is_connected(nx.to_undirected(g)):
            print('Átmérő:', nx.algorithms.distance_measures.diameter(g)
            print('Átlagos legrövidebb út:', nx.average_shortest_path_length(g))
        else:
            print('A gráf nem kapcsolódik össze teljesen, vannak izolált pontok, vagyis több komponensből áll. Ezért végtelen az átmérője és nem talál átlagos legrövidebb utat.')
                
        fig, ax = plt.subplots()
        
        #mu = sum(degrees)/len(degrees)
        #sigma = statistics.pstdev(degrees)
        
        ax.hist(degrees)
        ax.set_xlabel('Kapcsolatok száma')
        ax.set_ylabel('Elemek száma')
        ax.set_title(r'Fokszámeloszlás')


# In[67]:


def halozat():
    g = nx.read_edgelist("CA-GrQc.txt",create_using=nx.DiGraph(), nodetype = int)
    nx.draw(g)
    plt.show()
