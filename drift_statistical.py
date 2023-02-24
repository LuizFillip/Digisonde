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
    
def plotAll(avg, std, df):
    fig, ax = plt.subplots(figsize = (10, 4))
    #plotDays(ax, df)
    plotAgerage(ax, avg, std)
    
    ax.set(xticks = np.arange(0, 25, 2), 
           ylabel = "Velocidade (m/s)", 
           xlabel = "Hora universal")
    
    ax.legend(ncol = 3)
    
    return ax
    
def filter_values(avg, std, df1, std_factor = 1):
    
    out = []
    
    avg = avg.values
    std = std.values
    
    for col in df1.columns:
        
        arr = df1[col].values
        right = avg + (std_factor * std)
        left = avg - (std_factor * std)
    
        res = np.where((arr < right) & (arr > left), 
                       arr, np.nan)
        out.append(pd.DataFrame({col: res}, index = df1.index))
        
    return pd.concat(out, axis = 1)

df = load_drift(1, smoothed = False)

df["time"] = time2float(df.index.time)

df1 = pd.pivot_table(df, 
                    values = "vx", 
                    columns = df.index.date, 
                    index = "time")

avg = df1.mean(axis = 1)

std = df1.std(axis = 1)


new_ts = filter_values(avg, std, df1, std_factor = 2)
#print(new_ts)

ax = plotAll(avg, std, new_ts)
col = new_ts.columns[0]
ax.plot(new_ts[col])