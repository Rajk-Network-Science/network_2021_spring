import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import powerlaw as powerlaw

def suruseg_ertekelo(eloszl1, eloszl2):
    '''
    két eloszlásból megmondja, mennyi a legnagyobb abszolút különbség a sűrűségfüggvények között
    a bemeneti eloszlások pandas df oszlopai legyenek
    '''
    return np.abs(eloszl1.value_counts(normalize=True).sort_index() - eloszl2.value_counts(normalize=True).sort_index()).max()
    
def general_ertekel(n,p):
    '''
    generál egy binomiális eloszlást, melynek paraméterei n, p, 10000
    generál egy poisson eloszlást, melynek paraméterei n*p, 10000
    kiszámolja a kettő sűrűségfüggvényének maximális eltérését
    '''
    return np.abs(pd.DataFrame(np.random.binomial(n, p, 10000))[0].value_counts(normalize=True).sort_index() - pd.DataFrame(np.random.poisson(n*p, 10000))[0].value_counts(normalize=True).sort_index()).max()
    
def norm_konst(eloszl):
    '''
    kiszámolja egy eloszlásra a normalizációs konstans értékét, vagyis a hisztogram alatti területet
    '''
    values, bins, _ = plt.hist(eloszl)
    return sum(np.diff(bins)*values)
