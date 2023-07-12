import matplotlib.pyplot as plt
from Digisonde.drift import load_drift, get_month_avg
import numpy as np


def single_plot(ax, n, site, ext, col, smoothed, color, label):
    
    df = load_drift(n, 
                    site = site, 
                    ext = ext, 
                    smoothed = smoothed)
    
    mon_str = df.index[0].strftime("%B")
    
    ax.set(title = mon_str,
           xticks = np.arange(0, 24, 3))
    
    ax.axhline(0, linestyle = "--", color = "r")
    
    df1 = get_month_avg(df, col = col)

    df1 = df1.reindex(np.arange(0, 24, 1), 
                      method = "nearest")
    
    args = dict(color = color, capsize = 2)

    ax.errorbar(
        df1.index, 
        df1.mean(axis = 1), 
        yerr = df1.std(axis = 1), 
        **args, 
        label = label
        )
    
    return ax

def plot_monthly_averages(
        site = "SSA", 
        ext = "PRO", 
        col = "vz", 
        year = "2013", 
        smoothed = True
        ):
    
    
    fig, ax = plt.subplots(nrows = 3, 
                           ncols = 4, 
                           sharex = True, 
                           sharey = True, 
                           figsize = (16, 8))
    
    plt.subplots_adjust(wspace = 0.05)
    
    if col == "vz":
        name = "Deriva vertical"
        ylim = [-50, 50]
        
    elif col == "vx":
        name = "Deriva meridional"
        ylim = [-150, 150]
    else:
        name = "Deriva zonal"
        ylim = [-150, 150]
    
    for num in range(4):
        ax[2, num].set_xlabel("Hora (UT)", 
                              fontsize = 14)
        if num != 3:
            ax[num, 0].set_ylabel("Velocidade (m/s)", 
                                  fontsize = 14)
        
    
    es = ["RAW", "PRO"]
    cs = ["blue", "black"]
    ls = ["Brutos", "Processsados"]
    
    
    for n, ax in enumerate(ax.flatten(order = "F")):
        
        for a, ext in enumerate(es):
            ax1 = single_plot(ax, n, site, ext, col, smoothed, cs[a], ls[a])
            ax.set_ylim(ylim)
            
    fig.suptitle(f"{name} - São Luis - {year}")

    
    ax1.legend(ncol = 1,
               fontsize = 20,
               loc = "upper right", 
               bbox_to_anchor = (0.5, 3.6, 0.5, 0.5)
                     )
    
    
    return fig

def main():
    args = dict(
        site = "SSA", 
        ext = "PRO", 
        col = "vz", 
        smoothed = True
                )
    
    
    plot_monthly_averages(**args)



