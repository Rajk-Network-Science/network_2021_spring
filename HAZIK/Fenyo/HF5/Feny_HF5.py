import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
sns.set()
import networkx as nx
import gc
from statistics import mode

# from littleballoffur import SnowBallSampler - ez hibára fut
# import Graph_Sampling # Source of this package: https://github.com/Ashish7129/Graph_Sampling
# import random
# import time

# Random seed for reproduction
#random.seed(11)

# Read the data
'''
The source of this database: https://snap.stanford.edu/data/soc-Pokec.html
'''

DATAPATH = 'C:/Users/HP/Documents/02_CODING/KURZUS_Network/DATA/HF5'

def read_data_create_graph():
    '''
    This function reads the POKEC data and first generates the full graph, printing a simple analysis of it
    Then creates a subgraph with the edges where either of the nodes are from region nitriansky kraj, nitra, which is the second region with the most users in the graph
    The function also gives the nodes the attributes of age, gender and region, and returns the subgraph
    '''
    
    # Read the two text files
    rels = pd.read_csv(DATAPATH + '/soc-pokec-relationships.txt', sep = '\t', header = None)
    people = pd.read_csv(DATAPATH + '/soc-pokec-profiles.txt', sep = '\t', names = [x.strip() for x in list(pd.read_csv(DATAPATH + '/column_names.csv', header = None)[0])], index_col = False).rename(columns = {'AGE' : 'age'})
    people['gender2'] = ['male' if szam == 1 else 'female' for szam in people['gender'] ]
    people = people[['user_id', 'gender2', 'age', 'region']].rename(columns = {'gender2' : 'gender'})
    print('Data read successfully. \n \n')
    
    # Create the graph
    G = nx.Graph()
    G.add_edges_from(list(zip(rels[0], rels[1])))
    
    # Set attrubutes for gender, age and region
    nx.set_node_attributes(G, pd.Series(people.gender, index=people.user_id).to_dict(), 'gender')
    nx.set_node_attributes(G, pd.Series(people.age,    index=people.user_id).to_dict(), 'age')
    nx.set_node_attributes(G, pd.Series(people.region, index=people.user_id).to_dict(), 'region')
    
    print('Graph created successfully. \n')
    print('The number of nodes is: ', G.number_of_nodes())
    print('The number of edges is: ', G.number_of_edges())
    print('The average degree is: ', sum([d for n, d in G.degree]) / len([d for n, d in G.degree]), '\n \n')
    
    # Plot the degree distribution
    plt.figure()
    plt.hist(list(dict(G.degree).values()),
             bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200],
             edgecolor = 'white')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.title('Degree distribution in full network')
    plt.show()
    
    # Create subgraph
    subrels = rels[np.isin(rels.iloc[:,0], people[people['region'] == 'nitriansky kraj, nitra']['user_id']) & np.isin(rels.iloc[:,1], people[people['region'] == 'nitriansky kraj, nitra']['user_id'])]
    subG = nx.Graph()
    subG.add_edges_from(list(zip(subrels[0], subrels[1])))
    
    # Set attributes
    nx.set_node_attributes(subG, pd.Series(people.gender, index=people.user_id).to_dict(), 'gender')
    nx.set_node_attributes(subG, pd.Series(people.age,    index=people.user_id).to_dict(), 'age')
    nx.set_node_attributes(subG, pd.Series(people.region, index=people.user_id).to_dict(), 'region')

    print('Successfully created subgraph \n')
    print('The number of nodes is: ', subG.number_of_nodes())
    print('The number of edges is: ', subG.number_of_edges())
    print('The average degree is: ', sum([d for n, d in subG.degree]) / len([d for n, d in subG.degree]), '\n \n')
    
    # Plot the degree distribution
    plt.figure()
    plt.hist(list(dict(subG.degree).values()),
             bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200],
             edgecolor = 'white')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.title('Degree distribution in sample network')
    plt.show()
    
    del rels, people, G
    gc.collect()
    print('Dropped garbage.')
    
    return subG
    
def make_plots(subG):
    '''
    Creates analysing plots of networkx graph object.
    - Average degree by age
    - Average degree by age and gender
    - Average CC by age and gender
    - Average Neighbor Connectivity by age and gender
    '''
    
    plotdf = pd.DataFrame({
    'age' : [subG.nodes[x]['age'] for x in subG.nodes],
    'gender' : [subG.nodes[x]['gender'] for x in subG.nodes],
    'degree' : [subG.degree[x] for x in subG.nodes],
    'cc' : [nx.clustering(subG, x) for x in subG.nodes],
    'AND' : [list(nx.average_neighbor_degree(subG, nodes = [x]).values())[0] for x in subG.nodes]
    })

    fig, axes = plt.subplots(2,2, figsize = (10,10))
             
             
    axes[0,0].plot(plotdf[plotdf['age'] != 0].groupby('age').mean().iloc[14:65,:].index,
                plotdf[plotdf['age'] != 0].groupby('age').mean().iloc[14:65,:].degree.values)
    axes[0,0].set_xlabel('Age')
    axes[0,0].set_ylabel('Average degree')
    axes[0,0].set_title('Average number of POKEC friends')        
                
                
    axes[0,1].plot(plotdf[(plotdf['age'] != 0) & (plotdf['gender'] == 'male')].groupby('age').mean().iloc[14:65].index,
                plotdf[(plotdf['age'] != 0) & (plotdf['gender'] == 'male')].groupby('age').mean().iloc[14:65].degree.values,
                color = 'blue')
    axes[0,1].plot(plotdf[(plotdf['age'] != 0) & (plotdf['gender'] == 'female')].groupby('age').mean().iloc[14:65].index,
                plotdf[(plotdf['age'] != 0) & (plotdf['gender'] == 'female')].groupby('age').mean().iloc[14:65].degree.values,
                color = 'red')
    axes[0,1].set_xlabel('Age')
    axes[0,1].set_ylabel('Average degree')
    axes[0,1].set_title('Average number of POKEC friends')
    axes[0,1].legend(handles = [mpatches.Patch(color='red', label='Female'),
                        mpatches.Patch(color='blue', label='Male')])
                
    
    axes[1,0].plot(plotdf[(plotdf['age'] != 0) & (plotdf['gender'] == 'male')].groupby('age').mean().iloc[14:65].index,
                plotdf[(plotdf['age'] != 0) & (plotdf['gender'] == 'male')].groupby('age').mean().iloc[14:65].cc.values,
                color = 'blue')
    axes[1,0].plot(plotdf[(plotdf['age'] != 0) & (plotdf['gender'] == 'female')].groupby('age').mean().iloc[14:65].index,
                plotdf[(plotdf['age'] != 0) & (plotdf['gender'] == 'female')].groupby('age').mean().iloc[14:65].cc.values,
                color = 'red')
    axes[1,0].set_xlabel('Age')
    axes[1,0].set_ylabel('Average CC')
    axes[1,0].set_title('Triadic Closure')
    axes[1,0].legend(handles = [mpatches.Patch(color='red', label='Female'),
                                mpatches.Patch(color='blue', label='Male')])
                
                
    axes[1,1].plot(plotdf[(plotdf['age'] != 0) & (plotdf['gender'] == 'male')].groupby('age').mean().iloc[14:65].index,
                plotdf[(plotdf['age'] != 0) & (plotdf['gender'] == 'male')].groupby('age').mean().iloc[14:65].AND.values,
                color = 'blue')
    axes[1,1].plot(plotdf[(plotdf['age'] != 0) & (plotdf['gender'] == 'female')].groupby('age').mean().iloc[14:65].index,
                plotdf[(plotdf['age'] != 0) & (plotdf['gender'] == 'female')].groupby('age').mean().iloc[14:65].AND.values,
                color = 'red')
    axes[1,1].set_xlabel('Age')
    axes[1,1].set_ylabel('Average Neighbor Degree')
    axes[1,1].set_title('Neighbor Connectivity')
    axes[1,1].legend(handles = [mpatches.Patch(color='red', label='Female'),
                                mpatches.Patch(color='blue', label='Male')])
    
    plt.show()
    
    
def make_heatmaps(subG):
    '''
    Creates 4 heatmaps:
    - Connections between ages
    - M-M connections between ages
    - F-F connections between ages
    - M-F connections between ages
    '''
    
    fig, axes = plt.subplots(2,2, figsize = (10,10))
    
    kormatrix = {}
    # végigmegyünk a vizsgált életkorokon
    for i in range(15,41):
        # minden életkorra kilistázzuk az összes olyan életkorú embert, és nekik kilistázzuk az összes ismerősük életkorait
        ismerosok_korai = sum([[subG.nodes[node]['age'] for node in list(subG.neighbors(x))] for x in [node for node in subG.nodes if subG.nodes[node]['age'] == i]], [])
        # Ezekből az életkorokból kiszűrjük a nullákat, majd a 15-40 év közötti tartományt eltároljuk a kormátrixban
        kormatrix[i] = pd.Series([kor for kor in ismerosok_korai if kor != 0]).value_counts(bins = np.linspace(15,41,27), dropna = False).sort_index().values
        
    sns.heatmap([kormatrix[elem] for elem in kormatrix], square = True, ax = axes[0,0])
    axes[0,0].set(title = 'Korcsoportok közötti kapcsolatok száma')
    axes[0,0].set_xticklabels(np.linspace(15,41,13, dtype = int))
    axes[0,0].set_yticklabels(np.linspace(15,41,13, dtype = int), rotation = 0)
    
    
    # Férfiak közötti kapcsolatok
    kormatrix = {}
    # végigmegyünk a vizsgált életkorokon
    for i in range(15,41):
        # minden életkorra kilistázzuk az összes olyan életkorú FÉRFI nemű embert, és nekik kilistázzuk az összes FÉRFI ismerősük életkorait
        ismerosok_korai = sum([[subG.nodes[node]['age'] for node in list(subG.neighbors(x)) if subG.nodes[node]['gender'] == 'male'] for x in [nood for nood in [node for node in subG.nodes if subG.nodes[node]['age'] == i] if subG.nodes[nood]['gender'] == 'male']], [])
        # Ezekből az életkorokból kiszűrjük a nullákat, majd a 15-40 év közötti tartományt eltároljuk a kormátrixban
        kormatrix[i] = pd.Series([kor for kor in ismerosok_korai if kor != 0]).value_counts(bins = np.linspace(15,41,27), dropna = False).sort_index().values
        
    sns.heatmap([kormatrix[elem] for elem in kormatrix], square = True, ax = axes[0,1])
    axes[0,1].set(title = 'Férfiak közötti kapcsolatok száma')
    axes[0,1].set_xticklabels(np.linspace(15,41,13, dtype = int))
    axes[0,1].set_yticklabels(np.linspace(15,41,13, dtype = int), rotation = 0)
    
    
    # Nők közötti kapcsolatok
    kormatrix = {}
    # végigmegyünk a vizsgált életkorokon
    for i in range(15,41):
        # minden életkorra kilistázzuk az összes olyan életkorú NŐI nemű embert, és nekik kilistázzuk az összes NŐI ismerősük életkorait
        ismerosok_korai = sum([[subG.nodes[node]['age'] for node in list(subG.neighbors(x)) if subG.nodes[node]['gender'] == 'female'] for x in [nood for nood in [node for node in subG.nodes if subG.nodes[node]['age'] == i] if subG.nodes[nood]['gender'] == 'female']], [])
        # Ezekből az életkorokból kiszűrjük a nullákat, majd a 15-40 év közötti tartományt eltároljuk a kormátrixban
        kormatrix[i] = pd.Series([kor for kor in ismerosok_korai if kor != 0]).value_counts(bins = np.linspace(15,41,27), dropna = False).sort_index().values
        
    sns.heatmap([kormatrix[elem] for elem in kormatrix], square = True, ax = axes[1,0])
    axes[1,0].set(title = 'Nők közötti kapcsolatok száma')
    axes[1,0].set_xticklabels(np.linspace(15,41,13, dtype = int))
    axes[1,0].set_yticklabels(np.linspace(15,41,13, dtype = int), rotation = 0)
    
    
    # Férfiak és nők közötti kapcsolatok
    kormatrix = {}
    # végigmegyünk a vizsgált életkorokon
    for i in range(15,41):
        # minden életkorra kilistázzuk az összes olyan életkorú FÉRFI nemű embert, és nekik kilistázzuk az összes NŐI ismerősük életkorait
        ismerosok_korai = sum([[subG.nodes[node]['age'] for node in list(subG.neighbors(x)) if subG.nodes[node]['gender'] == 'female'] for x in [nood for nood in [node for node in subG.nodes if subG.nodes[node]['age'] == i] if subG.nodes[nood]['gender'] == 'male']], [])
        # Ezekből az életkorokból kiszűrjük a nullákat, majd a 15-40 év közötti tartományt eltároljuk a kormátrixban
        kormatrix[i] = pd.Series([kor for kor in ismerosok_korai if kor != 0]).value_counts(bins = np.linspace(15,41,27), dropna = False).sort_index().values
        
    sns.heatmap([kormatrix[elem] for elem in kormatrix], square = True, ax = axes[1,1])
    axes[1,1].set(title = 'Férfiak és Nők közötti kapcsolatok száma')
    axes[1,1].set_xticklabels(np.linspace(15,41,13, dtype = int))
    axes[1,1].set_yticklabels(np.linspace(15,41,13, dtype = int), rotation = 0)
    
    plt.show()
    
    
def base_gender_model(subG):
    '''
    Calculates the mode of genders for the neighbors of each node and prints the accuracy of this model
    '''
    print('A nemi megoszlás a hálózatban:')
    print(pd.Series([subG.nodes[node]['gender'] for node in subG.nodes]).value_counts(), '\n \n')
    print('A nemi megoszlás a becslés alapján:')
    print(pd.Series([mode([subG.nodes[node]['gender'] for node in list(subG.neighbors(x))]) for x in subG.nodes]).value_counts(), '\n \n')
    
    true_genders = [subG.nodes[node]['gender'] for node in subG.nodes]
    pred_genders = [mode([subG.nodes[node]['gender'] for node in list(subG.neighbors(x))]) for x in subG.nodes]
    
    precision = pd.Series([true_genders[i] == pred_genders[i] for i in range(len(true_genders))]).value_counts().values[1] / len(true_genders)
    print('A helyesen címkézett személyek aránya: %.3f' % precision)








