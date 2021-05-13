#!/usr/bin/env python
# coding: utf-8


# Csomagok importálása

import matplotlib
import networkx as nx
import csv
import matplotlib.pyplot as plt
import statistics
import numpy as np
import pandas as pd
import random


####################################################################################################
# általános megjegyzés: nem elegáns és nem is praktikus paraméter nélküli függvényeket megírni úgy,
# hogy belül tele vannak konstansokkal, helyette ezeket a konstansokat tedd be paraméternek
# itt egy példa:

def bad_func():
    
    return np.random.rand(2)

# helyett:

def good_func(x):
    
    return np.random.rand(x)

# és akkor, ha a fenti eredményt akarod, meghívod a függvényt így:

good_func(2)

# ilyen paraméterek pl.
# - az Erdős-Rényi gráf kezdeti csúcsainak száma és az élek sűrűsége
# - az egy iterációban hozzáadandó élek száma
# - copy modell esetén a p, stb.
####################################################################################################


COLORNODE = '#40a6d1'
COLOREDGE = '#5be732'


# Kezdeti Erdős-Rényi gráf (N = 30, p = 0,2)

def erdos_renyi():
    G= nx.erdos_renyi_graph(20,0.2) 
    nx.draw(G, with_labels=True) 
    plt.show()
    nx.draw(G, alpha = .3, edge_color = COLOREDGE, node_color = COLORNODE, node_size=50)


erdos_renyi()


# Kapcsolatválasztó modell

def link_selection():

    G= nx.erdos_renyi_graph(20,0.2)
    degrees = []
    normalised = []
    cluster = []
    for i in list(G.nodes):
        degrees.append(G.degree(i))
        
        # a networkx gráf class .degree() beépített methodja egy dictionary formában visszaadja az egyes csúcsok fokszámát
        # ezt listává lehet alakítani, és akkor nem kell for ciklust használni
        
    for i in degrees:
        normalised.append(i/(sum(degrees)))
        
        # ha numpy array-ekkel dolgozol listák helyett, akkor azokat egy utasításban le lehet osztani constanssal
        # nem kell végigiterálni az elemeiken
        # amúgy ezt a normalise-t megcsinálod, aztán valójában nem is használod
    
    for i in range(20, 1020):
        nodefix = list(G.nodes)
        G.add_node(i)
        
        # !!! ez nem a link selection algoritmus !!!
        # !!! olvasd el még egyszer a vonatkozó részt a könyvben, és implementáld a tényleges algoritmust !!!
        
        # egyébként ha az alábbi lenne a feladat, iteráció formájában kéne megcsinálni
        # képzeld mi lenne, ha egy körben nem +3, hanem +40 élt kéne hozzáadni, létrehoznál 40 új változót?
        
        a = random.choices(nodefix, weights=degrees, k=1)
        G.add_edge(a[0], i)
        b = random.choices(nodefix, weights=degrees, k=1)
        G.add_edge(b[0], i)
        c = random.choices(nodefix, weights=degrees, k=1)
        G.add_edge(c[0], i)
        
        degrees = []
        for x in list(G.nodes):
            degrees.append(G.degree(x))
            
            # na itt már használod a .degree() method-ot, de egyszerre is kikérhetnéd az összes node-ra
        
        normalised = []
        for y in degrees:
            normalised.append(y/(sum(degrees)))
        
        if i % 10 == 0:
            cluster.append((np.log(i))**2/(i))
            
            # !!! ez az elméleti összefüggés, amihez a klaszterezettség közelít BA hálózat esetén !!!
            # !!! neked az empirikusat kéne kiplottolnod, amit a legenerált hálózatodon mérsz !!!
            # !!! az 5.19-es ábrán a scatter plot az empirikus, a ráillesztett vonal pedig az elméleti !!!
        
    print('Csúcsok száma:', G.number_of_nodes())
    print('Klaszterezettségi együttható:', nx.average_clustering(G))
    print('Átlagos fokszám:', sum(degrees)/len(degrees))
    if nx.is_connected(nx.to_undirected(G)):
        
        # itt nem igazán értem, miért kell irányítatlanná alakítani a gráfot, amúgy is az
        # de egyébként az irányított gráfokra is lehet weakly és strongly connected feature-t számolni networkx-ben
        
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
    
    # ez egy plusz dolog, ha már mindent kijavítottál és marad időd:
    # a fokszámeloszlást nem hisztogramon szokás ábrázolni, hanem ahogyan a barabási könyvben van
    # log binekre kell osztani a fokszámokat, aztán log-log skálán, scatter ploton ábrázolni
    # lásd a könyv 4. fejezetének ezt a részét: http://networksciencebook.com/chapter/4#advanced-b
    
    fig, ax = plt.subplots()
                    
    ax.hist(cluster, bins = 50, log = True)
    ax.set_xlabel('Csúcsok száma')
    ax.set_ylabel('<C>')
    ax.set_title(r'Klaszterezettségi együttható')
    
    # !!! itt hisztogramot használni fogalomzavar !!!
    # !!! mindkét adatsorod egydimenziós, amit egymás ellen kiplottolsz: csúcsok száma és klaszterezettségi együttható !!!
    # !!! plusz, ugye már fentebb is írtam, hogy itt az empirikus megfigyelés kell, ne az elméleti függvényt ábrázold !!!


link_selection()


# Másolómodell


def copy_modell():

    G2= nx.erdos_renyi_graph(20,0.2)

    cluster2 = []
    p = 0.05
    egy_p = 1-p

    for i in range(20, 1020):
        
        # !!! a copy modellt sem implementáltad jól !!!
        # !!! olvasd el még egyszer figyelmesen a könyvben, hogy működik ez !!!
        
        floaty = random.random()
        G2.add_node(i)
        for g in range(3):
            if floaty < p:
                G2.add_edge(1, i) # !!! itt pl. mit keres ez a konstans 1? !!!
            else:
                G2.add_edge(random.choice(list(G2.nodes)), i)

        if i % 10 == 0:
            cluster2.append((np.log(i))**2/(i))
            
            # !!! innentől pedig egy az egyben ugyanazok a problémák vannak, amiket a link selection-nél is írtam !!!

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


copy_modell()


# Barabási-Albert modell


def B_M():
    
    # egy függvényen belül definiálsz két másik függvényt
    # ez azt jelenti, hogy minden egyes alkalommal, mikor meghívod a B_M-et, újra definiálja ezeket
    # ezért célszerű a B_A függvényen kívül definiálni őket
    # de amúgy nem is feltétlenül kell ezt a két mechanizmust plusz függvényekként definiálni,
    # mert csak a B_A-n belül használod őket
    
    def rand_prob_node():
        nodes_probs = []
        for node in G3.nodes():
            
            # ennél a for ciklusnál is lehet azt az egyszerűsítést alkalmazni, amit a link selectionnél írtam
            # plusz a G.number_of_edges() method visszaadja az élek számát
            
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
    
    # !!! nem teljes gráffal kezdődik a B_A algoritmus !!!
    # !!! csak az a kritérium, hogy mindegyik csúcsnak legyen legalább egy éle !!!
    # !!! így egy ideig nem is valósul meg a preferential attachment, mert minden csúcsnak ugyanannyi a fokszáma !!!
    # !!! bár ez nagy N mellett ez már nem számít, az elején még igen !!!
    # az algoritmus többi részét amúgy jól implementáltad

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

            # !!! innentől pedig egy az egyben ugyanazok a problémák vannak, amiket a link selection-nél is írtam !!!
            
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

B_M()
