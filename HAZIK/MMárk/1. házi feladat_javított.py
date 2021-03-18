#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import powerlaw as powerlaw
from sklearn import preprocessing


# Normalizációs konstans feladat

# In[39]:


prob_df=pd.DataFrame()

#próbáljuk meg ezt lerajzolni hisztogramon, ahogy az előbb
prob_df["power_2"]=powerlaw.Power_Law(xmin=2, parameters=[2],
                                      discrete=False).generate_random(10000)
prob_df["power_2_5"]=powerlaw.Power_Law(xmin=2, parameters=[2.5],discrete=False).generate_random(10000)
prob_df["power_3"]=powerlaw.Power_Law(xmin=2, parameters=[3],discrete=False).generate_random(10000)
prob_df["power_1_5"]=powerlaw.Power_Law(xmin=2, parameters=[1.5],discrete=False).generate_random(10000)
fig,axes=plt.subplots(2,2,figsize=(10,10))
row=0
col=0
for pl  in ["power_2","power_2_5","power_3","power_1_5"]:
    prob_df[pl].hist(bins=20,ax=axes[row,col])
    #axes[row,col].bar(x=prob_df[pl].unique(),height=prob_df[pl].value_counts().sort_index())
    axes[row,col].set_title(pl)
    if row==1:
        col+=1
        row=0
    else:
        row+=1
prob_df.head()
#fit = powerlaw.Fit(simulated_data)
#fit.power_law.xmin, fit.power_law.alpha


# In[40]:


fig,axes=plt.subplots(2,2,figsize=(10,10))
row=0
col=0
for pl  in ["power_2","power_2_5","power_3","power_1_5"]:
    np.log(prob_df[pl]).hist(bins=10,ax=axes[row,col])
    #axes[row,col].bar(x=prob_df[pl].unique(),height=prob_df[pl].value_counts().sort_index())
    axes[row,col].set_title(pl)
    #axes[row,col].set_yscale('log')

    if row==1:
        col+=1
        row=0
    else:
        row+=1


# In[41]:


norm_2 = prob_df["power_2"]/prob_df["power_2"].sum()
norm_2_5 = prob_df["power_2_5"]/prob_df["power_2_5"].sum()
norm_3 = prob_df["power_3"]/prob_df["power_3"].sum()
norm_1_5 = prob_df["power_1_5"]/prob_df["power_1_5"].sum()


# In[42]:


prob_normalized_df=pd.DataFrame()
prob_normalized_df["power_2_normalized"]=norm_2
prob_normalized_df["power_2_5_normalized"]=norm_2_5
prob_normalized_df["power_3_normalized"]=norm_3
prob_normalized_df["power_1_5_normalized"]=norm_1_5
prob_normalized_df


# In[43]:


#normalizációs konstansok
norm_2_allando = 1/sum(prob_df["power_2"])
norm_2_5_allando = 1/sum(prob_df["power_2_5"])
norm_3_allando = 1/sum(prob_df["power_3"])
norm_1_5_allando = 1/sum(prob_df["power_1_5"])
print(norm_2_allando)
print(norm_2_5_allando)
print(norm_3_allando)
print(norm_1_5_allando)


# In[44]:


#ellenőrzés
prob_normalized_df["power_2cum"]=prob_normalized_df["power_2_normalized"].cumsum()
prob_normalized_df["power_3cum"]=prob_normalized_df["power_2_5_normalized"].cumsum()
prob_normalized_df["power_2_5cum"]=prob_normalized_df["power_3_normalized"].cumsum()
prob_normalized_df["power_1_5cum"]=prob_normalized_df["power_1_5_normalized"].cumsum()
prob_normalized_df


# CHT feladat

# In[45]:


#előző random szám generálós megoldás
from numpy.random import seed
from numpy.random import randint

erteklista = []
atlaglista = []
for i in range(5000000):
    seed(i)
    erteklista.append(randint(0,1000))
step = 10 
for i, _ in enumerate(erteklista[::step]):
    intervallum = erteklista[i*10:] if (i+1)*10 > len(erteklista) else erteklista[i*10:(i+1)*10]
    atlaglista.append((sum(intervallum)/len(intervallum)))
print(atlaglista)


# In[46]:


#Random szám generálás nélküli sokkal gyorsabb megoldás.
from numpy.random import seed
from numpy.random import randint
import random

erteklista2 = []
atlaglista2 = []
for i in range(10000):
    erteklista2.append(i)
random.shuffle(erteklista2)
step = 10 

for i, _ in enumerate(erteklista2[::step]):
    intervallum = erteklista2[i*10:] if (i+1)*10 > len(erteklista2) else erteklista2[i*10:(i+1)*10]
    atlaglista2.append((sum(intervallum)/len(intervallum)))
print(atlaglista2)


# In[50]:


fig, ax = plt.subplots()
ax.hist(atlaglista2)
ax.set_title('Centrális határeloszlás')
ax.set_xlabel('Értékek')
ax.set_ylabel('Gyakoriság')


# Normál és Bernouli

# In[52]:


bern_df=pd.DataFrame()
np.random.seed(2)
bern_10=np.random.binomial(1,0.5,10)
bern_100=np.random.binomial(1,0.5,100)
bern_1000=np.random.binomial(1,0.5,1000)
bern_10000=np.random.binomial(1,0.5,10000)
bern_100000=np.random.binomial(1,0.5,100000)


# In[53]:


bern_10_avg=sum(bern_10)/len(bern_10)
bern_100_avg=sum(bern_100)/len(bern_100)
bern_1000_avg=sum(bern_1000)/len(bern_1000)
bern_10000_avg=sum(bern_10000)/len(bern_10000)
bern_100000_avg=sum(bern_100000)/len(bern_100000)

print(bern_10_avg)
print(bern_100_avg)
print(bern_1000_avg)
print(bern_10000_avg)
print(bern_100000_avg)


# In[54]:


normal_df10=pd.DataFrame()
normal_df100=pd.DataFrame()
normal_df1000=pd.DataFrame()
normal_df10000=pd.DataFrame()
normal_df100000=pd.DataFrame()

normal_df10["10"] = np.random.normal(0,1,10)
normal_df100["100"] = np.random.normal(0,1,100)
normal_df1000["1000"] = np.random.normal(0,1,1000)
normal_df10000["10000"] = np.random.normal(0,1,10000)
normal_df100000["100000"] = np.random.normal(0,1,100000)

print(normal_df10)
print(normal_df100)
print(normal_df1000)
print(normal_df10000)
print(normal_df100000)


# In[55]:


bins=np.linspace(-3,3,50)

normal_df10["10_binned"] = pd.cut(normal_df10["10"],bins=bins)
normal_df100["100_binned"] = pd.cut(normal_df100["100"],bins=bins)
normal_df1000["1000_binned"] = pd.cut(normal_df1000["1000"],bins=bins)
normal_df10000["10000_binned"] = pd.cut(normal_df10000["10000"],bins=bins)
normal_df100000["100000_binned"] =pd.cut(normal_df100000["100000"],bins=bins)


# In[56]:


density_df10=pd.DataFrame()
density_df100=pd.DataFrame()
density_df1000=pd.DataFrame()
density_df10000=pd.DataFrame()
density_df100000=pd.DataFrame()

density_df10["norm10"]=normal_df10["10_binned"].value_counts(normalize=True).sort_index()
density_df100["norm100"]=normal_df100["100_binned"].value_counts(normalize=True).sort_index()
density_df1000["norm1000"]=normal_df1000["1000_binned"].value_counts(normalize=True).sort_index()
density_df10000["norm10000"]=normal_df10000["10000_binned"].value_counts(normalize=True).sort_index()
density_df100000["norm100000"]=normal_df100000["100000_binned"].value_counts(normalize=True).sort_index()


# In[ ]:



fig,axes=plt.subplots(2,2,figsize=(10,10))
axes[0,0].plot(density_df10["norm10"])
axes[0,0].set_xlim(-3,3)
axes[0,0].set_title("Normal distribution 10")

axes[1,0].plot(density_df100["norm100"])
axes[1,0].set_xlim(-3,3)
axes[1,0].set_title("Normal distribution 100")

axes[0,1].plot(density_df1000["norm1000"])
axes[0,1].set_xlim(-3,3)
axes[0,1].set_title("Normal distribution 1000")

axes[1,1].plot(density_df10000["norm10000"])
axes[1,1].set_xlim(-3,3)
axes[1,1].set_title("Normal distribution 10000")


# Binomiális és Poisson eloszlás

# In[ ]:


#n*p=lam (p=lam/n), n->ထ => p->0


# In[58]:


prob_df["binom_10_10"]=np.random.binomial(10,0.001,10000)
prob_df["binom_100_10"]=np.random.binomial(100,0.001,10000)
prob_df["binom_500_10"]=np.random.binomial(500,0.001,10000)
prob_df["binom_5000_10"]=np.random.binomial(5000,0.001,10000)


print(prob_df["binom_10_10"].value_counts().sort_index())
print(prob_df["binom_100_10"].value_counts().sort_index())
print(prob_df["binom_500_10"].value_counts().sort_index())
print(prob_df["binom_5000_10"].value_counts().sort_index())


# In[59]:


prob_df["binom_10_10"].value_counts().sort_index()

lam_10_10 = sum(prob_df["binom_10_10"])/10000
lam_100_10 = sum(prob_df["binom_100_10"])/10000
lam_500_10 = sum(prob_df["binom_500_10"])/10000
lam_5000_10 = sum(prob_df["binom_5000_10"])/10000


print(lam_10_10)
print(lam_100_10)
print(lam_500_10)
print(lam_5000_10)


# In[60]:


prob_df["poi_10_10"]=np.random.poisson(lam_10_10,10000)
prob_df["poi_100_10"]=np.random.poisson(lam_100_10,10000)
prob_df["poi_500_10"]=np.random.poisson(lam_500_10,10000)
prob_df["poi_5000_10"]=np.random.poisson(lam_5000_10,10000)

prob_df


# In[61]:


fig,axes=plt.subplots(2,2,figsize=(10,5))

axes[0,0].bar(x=np.arange(11),height=pd.Series(index=np.arange(11),data=prob_df["poi_10_10"].value_counts().sort_index()).fillna(0))
axes[0,0].set_title("Poisson 10_10")

axes[0,1].bar(x=np.arange(11),height=pd.Series(index=np.arange(11),data=prob_df["poi_100_10"].value_counts().sort_index()).fillna(0))
axes[0,1].set_title("Poisson_100_10")

axes[1,0].bar(x=np.arange(11),height=pd.Series(index=np.arange(11),data=prob_df["poi_500_10"].value_counts().sort_index()).fillna(0))
axes[1,0].set_title("Poisson_500_10")

axes[1,1].bar(x=np.arange(11),height=pd.Series(index=np.arange(11),data=prob_df["poi_5000_10"].value_counts().sort_index()).fillna(0))
axes[1,1].set_title("Poisson_5000_10")

plt.tight_layout()


# In[62]:


fig,axes=plt.subplots(2,2,figsize=(10,5))

axes[0,0].bar(x=np.arange(11),height=pd.Series(index=np.arange(11),data=prob_df["binom_10_10"].value_counts().sort_index()).fillna(0))
axes[0,0].set_title("Poisson & Binominal 10_10")
axes[0,0].bar(x=np.arange(11),height=pd.Series(index=np.arange(11),data=prob_df["poi_10_10"].value_counts().sort_index()).fillna(0))

axes[0,1].bar(x=np.arange(11),height=pd.Series(index=np.arange(11),data=prob_df["binom_100_10"].value_counts().sort_index()).fillna(0))
axes[0,1].set_title("Poisson & Binominal 100_10")
axes[0,1].bar(x=np.arange(11),height=pd.Series(index=np.arange(11),data=prob_df["poi_100_10"].value_counts().sort_index()).fillna(0))

axes[1,0].bar(x=np.arange(11),height=pd.Series(index=np.arange(11),data=prob_df["binom_500_10"].value_counts().sort_index()).fillna(0))
axes[1,0].set_title("Poisson & Binominal 500_10")
axes[1,0].bar(x=np.arange(11),height=pd.Series(index=np.arange(11),data=prob_df["poi_500_10"].value_counts().sort_index()).fillna(0))

axes[1,1].bar(x=np.arange(11),height=pd.Series(index=np.arange(11),data=prob_df["binom_5000_10"].value_counts().sort_index()).fillna(0))
axes[1,1].set_title("Poisson & Binominal 5000_10")
axes[1,1].bar(x=np.arange(11),height=pd.Series(index=np.arange(11),data=prob_df["poi_5000_10"].value_counts().sort_index()).fillna(0))


# In[110]:


tiztiz = (prob_df["binom_10_10"]-prob_df["poi_10_10"]).value_counts().sort_index().fillna(0)
szaztiz = (prob_df["binom_100_10"]-prob_df["poi_100_10"]).value_counts().sort_index().fillna(0)
otszatiz = (prob_df["binom_500_10"]-prob_df["poi_500_10"]).value_counts().sort_index().fillna(0)
otezetiz = (prob_df["binom_5000_10"]-prob_df["poi_5000_10"]).value_counts().sort_index().fillna(0)

df_kulonbsegek = pd.DataFrame()
df_kulonbsegek["tiztiz"] = tiztiz
df_kulonbsegek["szaztiz"] = szaztiz
df_kulonbsegek["otszatiz"] = otszatiz
df_kulonbsegek["otezetiz"] = otezetiz
df_kulonbsegek


# In[101]:


fig,ax=plt.subplots(2,2,figsize=(10,5))
indx = np.arange(11)
ax[0,0].bar(x=np.arange(11), ax.bar(indx + bar_width/2), height=pd.Series(index=np.arange(11),data=prob_df["binom_10_10"].value_counts().sort_index()).fillna(0))

ax[0,0].bar(x=np.arange(11), ax.bar(indx - bar_width/2), height=pd.Series(index=np.arange(11),data=prob_df["poi_10_10"].value_counts().sort_index()).fillna(0))

