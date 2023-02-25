import pandas as pd
from Digisonde.drift_utils import load_drift
import matplotlib.pyplot as plt
from Digisonde.utils import time2float
import numpy as np

def plotDays(ax, df):

    for col in df.columns:
        ax.plot(df[col], lw = 0.5)

def plotAgerage(ax, avg, std):


    ax.plot(avg, label = "$\mu$", color = "k", lw = 2)
    ax.fill_between(avg.index, 
                    avg + std, 
                    avg - std, 
                    alpha = 0.3, label = "$\sigma$")
    
    ax.fill_between(avg.index, 
                    avg + 2 * std, 
                    avg - 2 * std, 
                    alpha = 0.3, label = "$2 \sigma$")
    
    ax.axhline(0, color = "red", linestyle = "--")
    
    ax.legend(ncol = 3)
    

    
def filter_values(avg, std, df1, std_factor = 1):
    
    out = []
    
    avg = avg.values
    std = std.values
    
    for col in df1.columns:
        
        arr = df1[col].values
        right = avg + (std_factor * std)
        left = avg - (std_factor * std)
    
        res = np.where((arr < right) & 
                       (arr > left), 
                       arr, np.nan)
        
        out.append(pd.DataFrame({col: res}, 
                                index = df1.index))
        
    return pd.concat(out, axis = 1)


def pivot_data(n, col = "vx"):

    df = load_drift(1, smoothed = False)
    
    month = df.index[0].strftime("%B")
    
    df["time"] = time2float(df.index.time)
    
    df1 = pd.pivot_table(df, 
                        values = col, 
                        columns = df.index.date, 
                        index = "time")
    
    return df1, month


def plotAverageAndDesviation(col = "vy", n = 1):
    
    df, month = pivot_data(n, col = col)
    
    avg = df.mean(axis = 1)
    
    std = df.std(axis = 1)
    
    if col == "vx":
        name = "meridional"
        lim = 200
    elif col == "vy":
        name = "zonal"
        lim = 300
    
    new_df = filter_values(avg, std, df, std_factor = 1)
    
    fig, ax = plt.subplots(figsize = (10, 8), 
                           nrows = 2, sharex = True, 
                           sharey = True)
    
    for n, d in enumerate([df, new_df]):
        
        plotAgerage(ax[n], avg, std)
        plotDays(ax[n], d)
    
        ax[n].set(ylabel = f"Velocidade {name} (m/s)")
        
    ax[0].set(title = f"{month} - São Luis")
    ax[1].set(xticks = np.arange(0, 25, 2),
              ylim = [-lim, lim],
              xlabel = "Hora universal")

