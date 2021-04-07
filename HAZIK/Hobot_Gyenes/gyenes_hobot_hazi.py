import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import community

header = ["user_id", "gender", "region", "AGE"]


def minta(df_node, df_attr):
    
    #kell neki adni headert

    header = ["user_id", "gender", "region", "AGE"]
    df_attr.columns=header
    df_node.columns=["node_1", "node_2"]
    
    #egy pár régiót választunk, ez a minta lényege
    
    df_attr=df_attr[(df_attr.region=="bratislavsky kraj, bratislava - nove mesto") | (df_attr.region=='bratislavsky kraj, bratislava - karlova ves') | (df_attr.region=='bratislavsky kraj, bratislava - ruzinov')]
    
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
    nana=nana.merge(df_attr, how="left", right_on="user_id", left_on="node_2")
    nana=nana[["node_1", "node_2", "gender_1", "gender_2", "age_1", "AGE"]]
    nana.columns=["node_1", "node_2", "gender_1", "gender_2", "age_1", "age_2"]
    nana=nana.drop_duplicates()



    
    return nana





def generate_attribute_data(data, G):
    da1=pd.DataFrame(G.nodes.data("gender_1"), columns=['Node',"Gender"])
    da2=pd.DataFrame(G.nodes.data("age_1"), columns=['Node',"Age"])
    da3=pd.DataFrame(G.degree(), columns=['Node',"Degree"])
    da4=pd.Series(nx.average_neighbor_degree(G)).to_frame().reset_index()
    da4.columns = ['Node',"Avg_Neighbor_Degree"]
    da5=pd.Series(nx.clustering(G)).to_frame().reset_index()
    da5.columns = ['Node',"Clustering_Coeff"]
    da6=pd.Series(nx.triangles(G)).to_frame().reset_index()
    da6.columns = ['Node',"Num_Triangles"]
    data=pd.merge(data, da1, how="inner", on="Node")
    data=pd.merge(data, da2, how="inner", on="Node")
    data=pd.merge(data, da3, how="inner", on="Node")
    data=pd.merge(data, da4, how="inner", on="Node")
    data=pd.merge(data, da5, how="inner", on="Node")
    data=pd.merge(data, da6, how="inner", on="Node")
    
    return data

def make_community(G):
    #a függvény lényege, hogy feltérképezzük a legközelebb álló "klasztereket" Louvain metódussal
    bestcomm_dict = community.best_partition(G)
    maxQ_L = community.modularity(bestcomm_dict,G)
    print("Klaszterek száma:", max(bestcomm_dict.values())+1, "Louvain modularitás: %.3f"%maxQ_L)
    
    return bestcomm_dict

def add_community(G, bestcomm_dict, data):
    # a függvény célja, hogy hozzáadjuk a gráf attributumokat tároló dataframehez a nodeokhoz tartozó communitiket
    commune=[]
    nodes=[]
    for node in G.nodes():
        commune.append(bestcomm_dict[node])
        nodes.append(node)
    communities=pd.DataFrame()
    communities["nodes"]=nodes
    communities["Community"]=commune
    data=data.merge(communities, how="left", left_on="Node", right_on="nodes")
    data.drop(["nodes"], axis=1)
    
    return data
    
    
def mean_predict(df):
    # a függvény lényege, hogy a szomszédok nemének móduszát adja az egyes node-ok prediktált nemére
    pred=df.groupby("node_1")[["gender_1","gender_2" ]].mean().reset_index()
    pred["predict"]=pred["gender_2"].apply(lambda half: 1 if half<0.5 else 0)
    
    return pred

def community_pred(data):
    com_pred=data.groupby(["Community"])["Gender"].mean().reset_index()
    com_pred.columns=["Community", "gender_com_pred"]
    com_pred=data.merge(com_pred, how="left", left_on="Community", right_on="Community")
    com_pred.gender_com_pred=com_pred.gender_com_pred.apply(lambda half: 1 if half<0.5 else 0)
    com_pred=com_pred[com_pred["Gender"].notna()]

    return com_pred

def triplet_pred(data):
    trip_pred=data
    trip_pred["Gender_pred"]=np.where(trip_pred["FF"]>trip_pred["LL"], 1, 0)
    trip_pred=trip_pred[trip_pred["Gender"].notna()]
    
    return trip_pred


def data_target(data):
    pred_data=data[data["Gender"].notna()].reset_index()
    pred_data=pred_data.drop("Gender", axis=1)
    target=data[data["Gender"].notna()].reset_index()
    target=target["Gender"]
    return pred_data, target


def plot_degree_dist(G, fit_line=False, expct_lo=1, expct_hi=10, expct_const=1):
    degree_hist = nx.degree_histogram(G) 
    degree_hist = np.array(degree_hist, dtype=float)
    degree_prob = degree_hist/G.number_of_nodes()
    plt.figure(figsize=(12, 8))
    plt.loglog(np.arange(degree_prob.shape[0]),degree_prob,linewidth = 0, marker = 'o', markersize = 4, color = 'purple', alpha = 1)
    if fit_line:
        w = [a for a in range(expct_lo,expct_hi)]
        z = []
        for i in w:
            x = (i**-3) * expct_const # Elméleti egyenes -3 meredekséggel és tetszőleges konstanssal
            z.append(x)
        plt.plot(w, z, 'k-', color='black')
    plt.xlabel('k')
    plt.ylabel('p(k)')
    plt.title('Degree Distribution')
    plt.show()
    
    
def triplets(data, G):
    triok=[]
    for n in G.nodes():
        dara=nx.to_pandas_edgelist(nx.ego_graph(G, n, radius=1, center=False))
        dara=dara.merge(data, how="left", left_on="target", right_on="Node")
        dara=dara.merge(data, how="left", left_on="source", right_on="Node")
        dara=dara[["Gender_x","Gender_y"]]
        dara=dara[dara['Gender_x'].notna()]
        dara=dara[dara['Gender_y'].notna()]
        dara=dara.reset_index()
        ff=0
        ll=0
        fl=0
        for i in range(len(dara)):
            if dara.loc[i][1]==0 and dara.loc[i][2]==0:
                ll+=1
            elif dara.loc[i][1]==1 and dara.loc[i][2]==1:
                ff+=1
            else:
                fl+=1
        szum=ff+ll+fl
        if ff>0:
            ff=ff/szum
        if ll>0:
            ll=ll/szum
        if fl>0:
            fl=fl/szum
        lista=[n,ff,ll,fl]
        triok.append(lista)

    triok=pd.DataFrame(triok, columns=['Node',"FF","LL","FL"])
    data=pd.merge(data, triok, how="inner", on="Node")

    return data



    
def age_degree(data):
    dara = data.pivot_table(index='Age', columns='Gender', values='Degree', aggfunc=np.nanmean).reset_index()
    dara.columns = ["Age","Women", "Men"]
    daka = data.pivot_table(index='Age', columns='Gender', values='Degree', aggfunc=np.nanstd).reset_index()
    daka.columns = ["Age","Women_error", "Men_error"]
    dara=pd.merge(dara, daka, how="inner", on="Age")
    Age=dara["Age"]
    Women=dara["Women"]
    Men=dara["Men"]
    Women_error=dara["Women_error"]
    Men_error=dara["Men_error"]
    plt.figure(figsize=(12, 8))
    plt.rc('font', family='serif', size=13)
    
    plt.plot(Age, Men, 'k', color='blue', label="Male")
    plt.fill_between(Age, Men-Men_error/Men, Men+Men_error/Men,
        alpha=0.5, edgecolor='#CC4F1B', facecolor='#089FFF')
    
    plt.plot(Age, Women, 'k', color='red', label="Female")
    plt.fill_between(Age, Women-Women_error/Women, Women+Women_error/Women,
        alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')
    
    plt.legend(loc='upper right')
    plt.xlabel('Age',fontsize=15)
    plt.ylabel('Average Degree',fontsize=15)
    plt.title("Degree Centrality")
    plt.xlim(13,40)

    
def age_connect(data):
    dara = data.pivot_table(index='Age', columns='Gender', values='Avg_Neighbor_Degree', aggfunc=np.nanmean).reset_index()
    dara.columns = ["Age","Women", "Men"]
    daka = data.pivot_table(index='Age', columns='Gender', values='Avg_Neighbor_Degree', aggfunc=np.nanstd).reset_index()
    daka.columns = ["Age","Women_error", "Men_error"]
    dara=pd.merge(dara, daka, how="inner", on="Age")
    Age=dara["Age"]
    Women=dara["Women"]
    Men=dara["Men"]
    Women_error=dara["Women_error"]
    Men_error=dara["Men_error"]
    plt.figure(figsize=(12, 8))
    plt.rc('font', family='serif', size=13)
    
    plt.plot(Age, Men, 'k', color='blue', label="Male")
    plt.fill_between(Age, Men-Men_error/Men, Men+Men_error/Men,
        alpha=0.5, edgecolor='#CC4F1B', facecolor='#089FFF')
    
    plt.plot(Age, Women, 'k', color='red', label="Female")
    plt.fill_between(Age, Women-Women_error/Women, Women+Women_error/Women,
        alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')
    
    plt.legend(loc='upper right')
    plt.xlabel('Age',fontsize=15)
    plt.ylabel('Average Neighbor Degree',fontsize=15)
    plt.title("Neighbor Connectivity")
    plt.xlim(13,40)
    
    
def age_clustering(data):
    dara = data.pivot_table(index='Age', columns='Gender', values='Clustering_Coeff', aggfunc=np.nanmean).reset_index()
    dara.columns = ["Age","Women", "Men"]
    daka = data.pivot_table(index='Age', columns='Gender', values='Clustering_Coeff', aggfunc=np.nanstd).reset_index()
    daka.columns = ["Age","Women_error", "Men_error"]
    dara=pd.merge(dara, daka, how="inner", on="Age")
    Age=dara["Age"]
    Women=dara["Women"]
    Men=dara["Men"]
    Women_error=dara["Women_error"]
    Men_error=dara["Men_error"]
    plt.figure(figsize=(12, 8))
    plt.rc('font', family='serif', size=13)
    
    plt.plot(Age, Men, 'k', color='blue', label="Male")
    plt.fill_between(Age, Men-Men_error/Men, Men+Men_error/Men,
        alpha=0.5, edgecolor='#CC4F1B', facecolor='#089FFF')
    
    plt.plot(Age, Women, 'k', color='red', label="Female")
    plt.fill_between(Age, Women-Women_error/Women, Women+Women_error/Women,
        alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')
    
    plt.legend(loc='upper right')
    plt.xlabel('Age',fontsize=15)
    plt.ylabel('Local clustering coefficient',fontsize=15)
    plt.title("Triadic Closure")
    plt.xlim(13,50)
    
    
    
    
def log_predict_data_target(df_attr):
    interesting=["hobbies", "hair_color", "body", "sign_in_zodiac", "relation_to_smoking", "relation_to_alcohol", "love_is_for_me", "I_like_specialties_from_kitchen", "gender"]
    interesting=df_attr[interesting]
    import warnings
    warnings.filterwarnings("ignore")
    #csinálok szlovák dolgokat
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


def boys_and_girls(df):
    cross_age=df[(df["age_1"]>15) & (df["age_2"]>15) & (df["age_2"]<35) & (df["age_1"]<35)]
    cross_age["age_1"]=cross_age['age_1'].fillna(0)
    cross_age["age_2"]=cross_age['age_2'].fillna(0)
    cross_age=cross_age.groupby(["age_1", "age_2"])["node_1"].count().unstack()
    cross_age=cross_age.fillna(0)

    cross_age_boys=df[(df["age_1"]>15) & (df["age_2"]>15) & (df["age_2"]<35) & (df["age_1"]<35) & (df["gender_1"]==1) & (df["gender_2"]==1)]
    cross_age_boys["age_1"]=cross_age_boys['age_1'].fillna(0)
    cross_age_boys["age_2"]=cross_age_boys['age_2'].fillna(0)
    cross_age_boys=cross_age_boys.groupby(["age_1", "age_2"])["node_1"].count().unstack()
    cross_age_boys=cross_age_boys.fillna(0)

    cross_age_girls=df[(df["age_1"]>15) & (df["age_2"]>15) & (df["age_2"]<35) & (df["age_1"]<35) & (df["gender_1"]==0) & (df["gender_2"]==0)]
    cross_age_girls["age_1"]=cross_age_girls['age_1'].fillna(0)
    cross_age_girls["age_2"]=cross_age_girls['age_2'].fillna(0)
    cross_age_girls=cross_age_girls.groupby(["age_1", "age_2"])["node_1"].count().unstack()
    cross_age_girls=cross_age_girls.fillna(0)

    cross_age_girls_boys=df[(df["age_1"]>15) & (df["age_2"]>15) & (df["age_2"]<35) & (df["age_1"]<35) & (df["gender_1"]==1) & (df["gender_2"]==0)]
    cross_age_girls_boys["age_1"]=cross_age_girls_boys['age_1'].fillna(0)
    cross_age_girls_boys["age_2"]=cross_age_girls_boys['age_2'].fillna(0)
    cross_age_girls_boys=cross_age_girls_boys.groupby(["age_1", "age_2"])["node_1"].count().unstack()
    cross_age_girls_boys=cross_age_girls_boys.fillna(0)

    return cross_age, cross_age_boys, cross_age_girls, cross_age_girls_boys


    
    
    
    
    
    
    
    
    
    