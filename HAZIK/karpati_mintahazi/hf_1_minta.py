import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns

LISTAK_SZAMA = 100
LISTAHOSSZ = 1000
P = 0.5
STDEV = P * (1 - P)


def generate_realization(lista_hossz, p):
    return pd.Series(np.random.binomial(1, p, lista_hossz))


def generate_experiment(listak_szama, lista_hossz, p):
    kiserlet = []
    for i in np.arange(listak_szama):
        kiserlet.append(generate_realization(lista_hossz, p))
    return pd.DataFrame(kiserlet)


def adjust_experiment_for_normal_distribution(kiserlet, p, stdev, lista_hossz):
    kiserlet["MEAN"] = kiserlet.mean(axis=1)
    kiserlet["MEAN_CENTRALIZED"] = kiserlet["MEAN"] - p
    kiserlet["MEAN_STANDARDIZED"] = kiserlet["MEAN_CENTRALIZED"] * np.sqrt(lista_hossz) / stdev
    return kiserlet


def plot_experiment(kiserlet):
    fig, axes = plt.subplots(1, 1)
    sns.distplot(kiserlet["MEAN_STANDARDIZED"], ax=axes)
    x = np.arange(-4, 4, 0.001)
    y = norm.pdf(x, 0, 1)
    axes.plot(x, y)
    return fig, axes


def generate_hazi_1(listak_szama, p, bins):
    listahosszok = [3,5,10,20,30,40,50,100]
    for lista_hossz in listahosszok:
        kiserlet = generate_experiment(listak_szama, lista_hossz, p)
        stdev = np.sqrt(p*(1-p))
        kiserlet = adjust_experiment_for_normal_distribution(kiserlet, p, stdev, lista_hossz)
        fig, axes = plot_experiment(kiserlet)
        fig.suptitle(f"N = {lista_hossz}")
    return kiserlet
