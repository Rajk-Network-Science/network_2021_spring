import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def LINK_rand_prob_node(G):
    a=np.random.randint(0,len(G.edges())) # Választok egy élt
    b=list(G.edges())[a] # Beteszem egy listába a pontokat
    random_proba_node=np.random.choice(b) # Kiválasztom az egyiket
    return random_proba_node



def add_edge(G, uj_csomopont):
    random_proba_node = LINK_rand_prob_node(G) # Meghívjuk a kiválasztott csomópontot
    new_edge = (random_proba_node, uj_csomopont) # Az új él a kiválasztott csomópont és az új csomópont között legyen majd
    if new_edge in G.edges(): # Ha van már él köztük, akkor válasszunk másik csomópontot a gráfból
        add_edge(G, uj_csomopont)
    else:
        G.add_edge(uj_csomopont, random_proba_node) # Adjuk hozzá a gráfhoz az új élt
    return G




def megoldas(G, N, kezdeti_csomopontok, m_parameter, count, uj_csomopont):
    for f in range(N - kezdeti_csomopontok):
        G.add_node(kezdeti_csomopontok + count)
        count += 1
        for e in range(0, m_parameter):
            add_edge(G,uj_csomopont)
        uj_csomopont += 1




def graf_abra(G):   
    pos = nx.kamada_kawai_layout(G)
    plt.figure(figsize=(12,12))
    
    sizes = [ 10*G.degree[node]+5 for node in G.nodes]
    
    #prlist = [ns_pr[node] for node in cnsG.nodes]
    
    nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color="r", edgecolors='#ffffff')
    
    nx.draw_networkx_edges(G, pos, edge_color='#00000088')
    
    # draw labels
    #labels = {node:cnsG.nodes[node]['name'] for node in prtop10}
    #nx.draw_networkx_labels(cnsG, ns_pos, labels=labels, font_size=12)
    
    plt.axis('off');




def k_distrib(graph, fit_line=False, expct_lo=1, expct_hi=10, expct_const=1):
    
    plt.close()
    num_nodes = graph.number_of_nodes()
    max_degree = 0
    
    # Megkeressük a legmagasabb fokszámot, ami alapján meghatározzuk az x-tengelyt
    for n in graph.nodes():
        if graph.degree(n) > max_degree:
            max_degree = graph.degree(n)
    
    # X és Y tengely értékei
    x = []
    y_tmp = []
    
    # Végigiterálok a legnagyobb fokszám terjedelmében és meghatározom az adott fokszámok arányait a csomópontok alapján
    for i in range(max_degree + 1):
        x.append(i)
        y_tmp.append(0)
        for n in graph.nodes():
            if graph.degree(n) == i:
                y_tmp[i] += 1
        y = [i / num_nodes for i in y_tmp] 
    
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Fokszám eloszlás (log-log scale)')
    plt.ylabel('log(P(k))')
    plt.xlabel('log(k)')
    plt.plot(x, y, linewidth = 0, marker = 'o', markersize = 4, color = 'purple', alpha = 1)
        
    if fit_line:
        w = [a for a in range(expct_lo,expct_hi)]
        z = []
        for i in w:
            x = (i**-3) * expct_const # Elméleti egyenes -3 meredekséggel és tetszőleges konstanssal
            z.append(x)
        plt.plot(w, z, 'k-', color='black')

    plt.show()