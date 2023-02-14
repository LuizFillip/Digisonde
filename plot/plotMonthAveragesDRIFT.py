import matplotlib.pyplot as plt
import pandas as pd
from Digisonde.statistical import load_drift, get_month_avg
import numpy as np



dates = pd.date_range("2013-1-1", 
                      "2013-12-31", 
                      freq = "1M")
df = load_drift()

fig, ax = plt.subplots(nrows = 3, 
                       ncols = 4, 
                       sharex = True, 
                       sharey = True, 
                       figsize = (16, 10))

plt.subplots_adjust(wspace = 0.05)

for num in range(4):
    ax[2, num].set_xlabel("Hora (UT)", fontsize = 14)
    if num != 3:
        ax[num, 0].set_ylabel("Velocidade (m/s)", fontsize = 14)
    
for n, ax in enumerate(ax.flatten(order = "F")):
    
    mon_str = dates[n].strftime("%B")
    
    ax.set(title = mon_str, xticks = np.arange(0, 24, 3))
    
    ax.axhline(0, linestyle = "--", color = "r")
    
    df1 = get_month_avg(df, n, col = "vz")
    
    new_idx = pd.Index(np.arange(0, 24, 0.5))
    
    df1 = df1.reindex(new_idx, method = "nearest")
    
    args = dict(color = "k", capsize = 2)

    ax.errorbar(df1.index, 
                df1.mean(axis = 1), 
                yerr = df1.std(axis = 1), 
                **args)