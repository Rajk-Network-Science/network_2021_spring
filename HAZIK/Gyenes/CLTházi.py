import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from wand.image import Image
from wand.display import display
import seaborn as sns
import scipy
import scipy.stats as stats
%matplotlib notebook

E=1/6*(1+2+3+4+5+6)
print("Expected value=",E)

# 1000 simulations of die roll
n = 10000

avg = []
#10-esével 10-től n-ig
for i in range(10,n,10):
    avg.append(np.average(np.random.randint(1,7,10)))

n=100
avg=[]
for i in range(n):
    avg.append(np.average(np.random.randint(1,7,10)))

def clt(current):
    # if animation is at the last frame, stop it
    plt.cla()
    if current == len(avg): 
        a.event_source.stop()

    #fit = stats.norm.pdf(avg[0:current], np.mean(avg[0:current]), np.std(avg[0:current]))
    #plt.plot(avg[0:current], fit, label="Probality Density Function")
    #plt.plot(avg[0:current], fit,'r-', lw=7, alpha=0.6, label='norm pdf')
    x = 
    y = norm.pdf(x,0,1)
    plt.plot()
    
    sns.distplot(avg[0:current],
                 hist=False,
                 kde=True,
                 kde_kws={'shade':True,"color": "k", "lw": 3, "label": "Density of Samples"},
                 norm_hist=True)   
    plt.legend(loc='upper right')
    plt.gca().set_title('Expected value of die rolls')
    plt.gca().set_xlabel('Average from die roll')
    plt.gca().set_ylabel('Frequency')
    plt.annotate('Die roll = {}'.format(current*10+10), [4.5,0.4], color="red")

fig = plt.figure()
a = animation.FuncAnimation(fig, clt, interval=10)