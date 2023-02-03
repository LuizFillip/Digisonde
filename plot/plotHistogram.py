import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plotHistogram(year = 2015, col= "vzp"):
    
    infile = f"database/drift/{year}.txt"

    df = pd.read_csv(infile, index_col = 0)

    df.index = pd.to_datetime(df.index)
    
    fig, ax = plt.subplots(figsize = (6, 4))

    lmax = round(df.max().max())
    lmin = round(df.min().min())

    binwidth = 5

    bins = np.arange(lmin, 
                     lmax + binwidth, 
                     binwidth)

    ax.set(title = "Velocidade do PRE", 
           xlabel = "Velocidade (m/s)",
           ylabel = "Número de eventos",
           xlim = [lmin - binwidth, 
                    lmax + binwidth])

    args = dict(facecolor = 'lightgrey', 
                alpha = 1, 
                edgecolor = 'black', 
                hatch = '////', 
                color = 'gray', 
                linewidth = 1)


    df[col].hist(bins = bins, 
                   ax = ax, **args)
     
    plot_stats(ax, df[col])
    
    plt.show()
    
    
def plot_stats(ax, data, unit = "m/s"):
    mean = round(data.mean(), 2)
    std = round(data.std(), 2)
    
    info_mean = f"$<V_z> = {mean}$ {unit}\n"
    info_std = f"  $\sigma = {std}$ {unit}"
    
    ax.text(0.4, 0.7, info_mean + info_std, 
            fontsize = 15, 
            transform = ax.transAxes)
    
   
plotHistogram(year = 2019)
    
    
