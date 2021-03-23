import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import time

# Random seed for reproduction
random.seed(11)

# Create base ER graph
ER = nx.erdos_renyi_graph(20,0.2, seed = 11)

# Create ER graph data for comparison
def ER_comparison(n):
    log = {'N' : [], 'avgC' : []}
    for i in range(n):
        if i % 10 == 0:
            ER = nx.erdos_renyi_graph(20+i,0.2, seed = 11)
            log['N'].append(20+i+1)
            log['avgC'].append(nx.average_clustering(ER))
    return ER, log

# Link selection model
def link_selection(G, n):
    '''
    Adds n random new nodes to networkx object G, with edges calculated like this
    - choose a random edge from G
    - choose one of the nodes
    - do this 3 times
    - the new node will connect to these 3 nodes
    - every 10 steps stores avg clustering coefficient and current N (number of nodes)
    '''
    log = {'N' : [], 'avgC' : []}
    H = G.copy()
    for i in range(n):
        H.add_node(1000+i)
        for j in range(3):
            H.add_edge(1000+i, random.choice(random.choice(list(H.edges))))
        if i % 10 == 0:
            log['N'].append(20+i+1)
            log['avgC'].append(nx.average_clustering(H))
    return H, log
    
# Copy model
def copy_algorithm(G, n):
    '''
    Adds n random new nodes to networkx object G, with edges calculated like this
    - create a new node
    - choose a random node from G, but not the new node
    - with probability p (which is 1/N) create a new edge between this node and new node
    - with probabilty 1-p create a new edge between a random neighbor of the random node and new node
    - do this 3 times
    - every 10 steps stores avg clustering coefficient and current N (number of nodes)
    '''
    log = {'N' : [], 'avgC' : []}
    H = G.copy()
    for i in range(n):
        H.add_node(1000+i)
        random_node = random.choice([csucs for csucs in list(H.nodes()) if csucs != 1000+i]) # we have to prevent choosing the new node!
        for j in range(3):
            if random.random() < (1/len(H.nodes())-1): # -1 because a new node is already present
                H.add_edge(1000+i, random_node)
            else:
                H.add_edge(1000+i, random.choice(list(H.edges(random_node)))[1])
        if i % 10 == 0:
            log['N'].append(20+i+1)
            log['avgC'].append(nx.average_clustering(H))
    return H, log

# BA model
def ba_model(G, n):
    '''
    Adds n random new edges to a networkx object G, with edges calculated like this:
    - choose 3 random nodes from G where each node has probabilty with weights of degree to be chosen
    - add a new node and add 3 edges between this new node and the chosen 3 nodes
    - every 10 steps stores avg clustering coefficient and current N (number of nodes)
    '''
    log = {'N' : [], 'avgC' : []}
    H = G.copy()
    for i in range(n):        
        chosen = random.choices(
                    population = list(dict(H.degree).keys()),
                    weights = list(dict(H.degree).values()),
                    k = 3)
        H.add_node(1000+i)
        for node in chosen:
            H.add_edge(1000+i, node)
        if i % 10 == 0:
            log['N'].append(20+i+1)
            log['avgC'].append(nx.average_clustering(H))
    return H, log

def create_graphs(n):
    print('The chosen number of additional nodes to base 20 is ', n)
    ERcomp, ERlog = ER_comparison(n)
    print('Created comparison info of ER graph')
    link, log1 = link_selection(ER, n)
    print('Created graph with link selection')
    copy, log2 = copy_algorithm(ER, n)
    print('Created graph with copy model')
    ba, log3 = ba_model(ER, n)
    print('Created graph with BA model')
    return ERcomp, ERlog, link, log1, copy, log2, ba, log3
    
def visualize_graphs(ERcomp, ERlog, link, log1, copy, log2, ba, log3):
    
    # Base ER with 20 nodes
    plt.rcParams["figure.figsize"] = (5,5)
    nx.draw(ER, with_labels = True)
    plt.title('Alap 20 csúcsú, 40 élű ER gráf', fontsize = 14)
    plt.show()
    
    # Color map: same for all graphs
    color_map = []
    for node in link:
        if node >= 1000:
            color_map.append('green')
        else: 
            color_map.append('blue')
            
    # Link selection
    plt.rcParams["figure.figsize"] = (5,5)
    nx.draw_shell(link,
            with_labels = False,
            node_color = color_map,
            node_size = 20,
            alpha = 0.3)
    plt.title('Link selection algoritmussal generált gráf', fontsize = 14)
    plt.show()
    
    # Copy
    plt.rcParams["figure.figsize"] = (5,5)
    nx.draw_shell(copy,
            with_labels = False,
            node_color = color_map,
            node_size = 20,
            alpha = 0.3)
    plt.title('Copy algoritmussal generált gráf', fontsize = 14)
    plt.show()
    
    # BA
    plt.rcParams["figure.figsize"] = (5,5)
    nx.draw_shell(ba,
            with_labels = False,
            node_color = color_map,
            node_size = 20,
            alpha = 0.3)
    plt.title('BA modell szerint generált gráf', fontsize = 14)
    plt.show()
    
def avg_clustering_plot(ERcomp, ERlog, link, log1, copy, log2, ba, log3):
    plt.scatter(np.log(log1['N']), log1['avgC'], color = 'red', label = 'link')
    plt.scatter(np.log(log2['N']), log2['avgC'], color = 'blue', label = 'copy')
    plt.scatter(np.log(log3['N']), log3['avgC'], color = 'yellow', label = 'BA')
    plt.scatter(np.log(ERlog['N']), ERlog['avgC'], color = 'black', label = 'ER')
    plt.legend()
    plt.xlabel('A gráfban található csúcsok számának logaritmusa', fontsize = 14)
    plt.ylabel('Az átlagos klaszterezettségi együttható', fontsize = 14)
    
    
    
    
    
    
    
    
    
    
    
    
    
    