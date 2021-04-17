import pandas as pd

def country_dict(conti):
    lista=[]
    for group in conti.groupby("Continent")["Country"]:
        lista.append(group)

    conti_dict={}
    for i in range(len(lista)):
        conti_dict[lista[i][0]]=list(lista[i][1])

    return conti_dict