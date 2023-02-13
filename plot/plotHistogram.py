import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load( year = 2015, col= "vzp"):
    infile = f"database/drift/{year}.txt"

    df = pd.read_csv(infile, index_col = 0)

    df.index = pd.to_datetime(df.index)
    return df


def plotHistogram(arr):

    fig, ax = plt.subplots(figsize = (6, 4))

    lmax = round(arr.max())
    lmin = round(arr.min())

    binwidth = 10

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


    ax.hist(arr, bins = bins, **args)
     
    plot_stats(ax, arr)
    
    return fig
    
    
def plot_stats(ax, data, unit = "m/s"):
    mean = round(data.mean(), 2)
    std = round(data.std(), 2)
    
    info_mean = f"$<V_z> = {mean}$ {unit}\n"
    info_std = f"  $\sigma = {std}$ {unit}"
    
    ax.text(0.05, 0.7, info_mean + info_std, 
            fontsize = 15, 
            transform = ax.transAxes)
    
   
#
    
from Digisonde.statistical import load_drift, get_month_avg

df = load_drift()


col = "vz"

vz_limits = (-100, 100)


cond_limits = ((df[col] > vz_limits[0]) &  
             (df[col] < vz_limits[-1]))


df = df.loc[(df.index.month == 1) & cond_limits]



arr = df["vx"].values

plotHistogram(arr)
    
