import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re

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
    "more"
]

def megnyit(filename):
    df = pd.read_csv(filename, compression='gzip', header=None, sep='\t', quotechar='"')
    return df

def minta(df_node, df_attr):
    
    #kell neki adni headert
    df_attr.columns=header
    df_node.columns=["node_1", "node_2"]
    
    #dobjuk ki a szart a picsába
    df_attr=df_attr[df_attr.region=="bratislavsky kraj, bratislava - nove mesto"]
    
    #itt lesz pár merge
    na=df_attr.merge(df_node, left_on="user_id", right_on="node_1", how="inner")
    nana=pd.DataFrame()
    nana["user_id"]=na["user_id"]
    nana["gender"]=na["gender"]
    nana=nana.merge(na, how="left", right_on="node_2", left_on="user_id")
    nana = nana[nana['node_1'].notna()]
    nana.drop_duplicates()
    nana=nana[["node_1", "node_2", "gender_y", "gender_x", "AGE"]]
    nana.columns=["node_1", "node_2", "gender_1", "gender_2", "age_1"]
    
    return nana

    
    
def mean_predict(df):
    pred=df.groupby("node_1")[["gender_1","gender_2" ]].mean().reset_index()
    pred["predict"]=pred["gender_2"].apply(lambda half: 1 if half<0.5 else 0)
    
    return pred




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
    plt.title('Degree Distribution (log-log scale)')
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
    
    
    
def age_degree(G):
    plt.close()
    
    # X és Y tengely értékei
    kor=[]
    for i in G.nodes.data("age_1"):
        kor.append(i[1])
    
    x=set(kor)
    x=list(x)
    if None in x:
        x.remove(None)
    y1 = []
    y2 = []
    
    # Végigiterálok a kor terjedelmében és meghatározom az adott fokszámok arányait a csomópontok alapján
    for i in x:
        y_tmp1=[]
        y_tmp2=[]
        for n in G.nodes():
            if G.nodes.data("age_1")[n]==i:
                if G.nodes.data("gender_1")[n]==1:
                    y_tmp1.append(G.degree[n])
                elif G.nodes.data("gender_1")[n]==0:
                    y_tmp2.append(G.degree[n])
                else:
                    pass
            else:
                pass
        if len(y_tmp1)>0:
            y1.append(np.nanmean(y_tmp1))
        else:
            y1.append(0)
        if len(y_tmp2):
            y2.append(np.nanmean(y_tmp2))
        else:
            y2.append(0)
    
    x = np.array(x)
    y1 = np.array(y1)
    y2 = np.array(y2)
    y=[]
    y.append(np.nanmax(y1))
    y.append(np.nanmax(y2))
    y.append(np.nanmin(y1))
    y.append(np.nanmin(y2))
    
    plt.rc('font', family='serif', size=13)
    plt.plot(x,y1, linewidth = 1, marker = 'o', markersize = 4,label="Male", color='#0066FF')
    plt.plot(x,y2, linewidth = 1, marker = 'o', markersize = 4,label="Female", color='red')
    plt.xlabel('Age',fontsize=15)
    plt.ylabel('Average Degree',fontsize=15)
    plt.title("Degree Centrality")
    plt.xlim(13,40)
    plt.ylim(np.min(y),np.max(y))
    plt.legend(loc='lower left')
    plt.show()   
    

    
def age_connect(G):
    plt.close()
    # X és Y tengely értékei
    kor=[]
    for i in G.nodes.data("age_1"):
        kor.append(i[1])
    x=set(kor)
    x=list(x)
    if None in x:
        x.remove(None)
    y1 = []
    y2 = []
    # Végigiterálok a kor terjedelmében és meghatározom az adott fokszámok arányait a csomópontok alapján
    for i in x:
        y_tmp1=[]
        y_tmp2=[]
        for n in G.nodes():
            if G.nodes.data("age_1")[n]==i:
                if G.nodes.data("gender_1")[n]==1:
                    y_tmp1.append(nx.average_neighbor_degree(G)[n])
                elif G.nodes.data("gender_1")[n]==0:
                    y_tmp2.append(nx.average_neighbor_degree(G)[n])
                else:
                    pass
            else:
                pass
        if len(y_tmp1)>0:
            y1.append(np.nanmean(y_tmp1))
        else:
            y1.append(0)
        if len(y_tmp2):
            y2.append(np.nanmean(y_tmp2))
        else:
            y2.append(0)
    x = np.array(x)
    y1 = np.array(y1)
    y2 = np.array(y2)
    y=[]
    y.append(np.nanmax(y1))
    y.append(np.nanmax(y2))
    y.append(np.nanmin(y1))
    y.append(np.nanmin(y2))
    plt.rc('font', family='serif', size=13)
    plt.plot(x,y1, linewidth = 1, marker = 'o', markersize = 4,label="Male", color='#0066FF')
    plt.plot(x,y2, linewidth = 1, marker = 'o', markersize = 4,label="Female", color='red')
    plt.xlabel('Age',fontsize=15)
    plt.ylabel('Average Neighbor Degree',fontsize=15)
    plt.title("Neighbor Connectivity")
    plt.xlim(13,40)
    plt.ylim(np.min(y),np.max(y))
    plt.legend(loc='lower left')
    plt.show()      
    
def age_clustering(G):
    plt.close()
    # X és Y tengely értékei
    kor=[]
    for i in G.nodes.data("age_1"):
        kor.append(i[1])
    x=set(kor)
    x=list(x)
    if None in x:
        x.remove(None)
    y1 = []
    y2 = []
    # Végigiterálok a kor terjedelmében és meghatározom az adott fokszámok arányait a csomópontok alapján
    for i in x:
        y_tmp1=[]
        y_tmp2=[]
        for n in G.nodes():
            if G.nodes.data("age_1")[n]==i:
                if G.nodes.data("gender_1")[n]==1:
                    y_tmp1.append(nx.clustering(G)[n])
                elif G.nodes.data("gender_1")[n]==0:
                    y_tmp2.append(nx.clustering(G)[n])
                else:
                    pass
            else:
                pass
        if len(y_tmp1)>0:
            y1.append(np.nanmean(y_tmp1))
        else:
            y1.append(0)
        if len(y_tmp2):
            y2.append(np.nanmean(y_tmp2))
        else:
            y2.append(0)
    x = np.array(x)
    y1 = np.array(y1)
    y2 = np.array(y2)
    y=[]
    y.append(np.nanmax(y1))
    y.append(np.nanmax(y2))
    y.append(np.nanmin(y1))
    y.append(np.nanmin(y2))
    plt.rc('font', family='serif', size=13)
    plt.plot(x,y1, linewidth = 1, marker = 'o', markersize = 4,label="Male", color='#0066FF')
    plt.plot(x,y2, linewidth = 1, marker = 'o', markersize = 4,label="Female", color='red')
    plt.xlabel('Age',fontsize=15)
    plt.ylabel('Local clustering coefficient',fontsize=15)
    plt.title("Triadic Closure")
    plt.xlim(13,40)
    plt.ylim(np.min(y),np.max(y))
    plt.legend(loc='lower left')
    plt.show()
    
    
    
    
    
def log_predict_data_target(df_attr):
    interesting=["hobbies", "hair_color", "body", "sign_in_zodiac", "relation_to_smoking", "relation_to_alcohol", "love_is_for_me", "I_like_specialties_from_kitchen", "gender"]
    interesting=df_attr[interesting]
    import warnings
    warnings.filterwarnings("ignore")
    #csináélok szlovák dolgokat
    interesting["sex"]=np.where(interesting.hobbies.str.contains("sex"), 1, 0)
    interesting["kino"]=np.where(interesting.hobbies.str.contains("kino"), 1, 0)
    interesting["spanie"]=np.where(interesting.hobbies.str.contains("spanie"), 1, 0)
    interesting["turistika"]=np.where(interesting.hobbies.str.contains("turistika"), 1, 0)
    interesting["jedlo"]=np.where(interesting.hobbies.str.contains("jedlo"), 1, 0)
    interesting["citanie"]=np.where(interesting.hobbies.str.contains("citanie"), 1, 0)
    interesting["tancovanie"]=np.where(interesting.hobbies.str.contains("tancovanie"), 1, 0)
    interesting["prace okolo domu"]=np.where(interesting.hobbies.str.contains("prace okolo domu"), 1, 0)
    interesting["praca s pc"]=np.where(interesting.hobbies.str.contains("praca s pc"), 1, 0)
    interesting["pracemiluju slovaky"]=np.where(interesting.hobbies.str.contains("pracemiluju slovaky"), 1, 0)
    interesting["pozeranie filmov"]=np.where(interesting.hobbies.str.contains("pozeranie filmov"), 1, 0)
    interesting["kupalisko"]=np.where(interesting.hobbies.str.contains("kupalisko"), 1, 0)
    interesting["stanovanie"]=np.where(interesting.hobbies.str.contains("stanovanie"), 1, 0)
    interesting["sportovanie"]=np.where(interesting.hobbies.str.contains("sportovanie"), 1, 0)
    interesting["smoking"]=np.where(interesting.relation_to_smoking.str.contains("ne"), 0, 1)
    interesting["love"]=np.where(interesting.love_is_for_me.str.contains("ne"), 0, 1)
    interesting["weight"]=interesting["body"].apply(lambda body: re.findall(r"( \d\d )", str(body)))
    interesting["weight"]=interesting["weight"].apply(lambda weight: int(weight[0]) if len(weight)==1 else np.nan)
    interesting["height"]=interesting["body"].apply(lambda body: re.findall(r"( \d\d\d )", str(body)))
    interesting["height"]=interesting["height"].apply(lambda height: int(height[0]) if len(height)==1 else np.nan)
    
    #drop üres célváltozó
    interesting = interesting[interesting['gender'].notna()]
    interesting["gender"]=interesting["gender"].apply(lambda gender: int(gender))
    
    #hátha van magyarázó értelme annak, hogy kik nem töltik ki
    interesting["missing_height"]=np.where(interesting.height.isna(), 1, 0)
    interesting["missing_weight"]=np.where(interesting.weight.isna(), 1, 0)
    
    #target és data
    data=interesting.iloc[:,-18:]
    target=interesting["gender"]
    
    #mostmár jöhetnek a fillna-k.
    data["height"]=data["height"].fillna(interesting.height.mean())
    data["weight"]=data["weight"].fillna(interesting.weight.mean())
    data["height"]=data["height"].apply(lambda height: int(height))
    data["weight"]=data["weight"].apply(lambda weight: int(weight))
    
    return data,target
    
    
    
    
    
    
    
    
    
    