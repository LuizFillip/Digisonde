import pandas as pd
from build import paths as p
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import datetime as dt
from FabryPerot.core import load


def func(x, a, c):
    return a * x + c



def join_data(time = dt.time(22, 0, 0),
              month = 1, 
              direction = "Meridional"):
    
    drift = load_drift(folder = "Drift", 
                       subfolder = "SSA", 
                       col = "vx")

    fpi = load(p("FabryPerot").get_files_in_dir("processed"))

    coords = {"Meridional": ("vx", "mer"), 
              "Zonal": ("vy", "zon")}
    
    sel_dri, sel_fpi = coords[direction]
    
    def sel_data(df, time, col):
        df = df.loc[~df.index.duplicated(keep='first')]
        return df.loc[df.index.time == time, col]
    
    sel_fpi = fpi.loc[(fpi.index.month == month) & 
                  (fpi.index.time == time), [sel_fpi]]
    
    sel_drift = drift.loc[(drift.index.month == month) & 
                    (drift.index.time == time), [sel_dri]]
    
    join = pd.concat([sel_fpi, sel_drift], axis = 1).dropna()
    
    join.columns = ["FPI", "DRIFT"]
    
    return join


def plotScatter(ax, join):
    
    date = join.index[0].strftime("%B")
    
    xdata = join["FPI"].values
    ydata = join["DRIFT"].values
    
    
    ax.plot(xdata, ydata, color = "k",
             linestyle = "none", marker = "o")
    
    ax.set(title = f"{date}")
    
    
    popt, pcov = curve_fit(func, xdata, ydata)
    
    ax.grid()
    ax.plot(xdata, func(xdata, *popt), 
            'r-',
             label='a=%5.2f, c=%5.2f' % tuple(popt))
    
    ax.legend()

def plot_scatter_corr(direction = "Zonal", 
         time = dt.time(21, 0, 0)):
    
    fig, ax = plt.subplots(figsize = (14, 8), 
                           ncols = 4,
                           nrows = 3, 
                           sharey = True, 
                           sharex = True)
    
    plt.subplots_adjust(hspace = 0.2, 
                        wspace = 0.1)
    
    
    
    for n, ax in enumerate(ax.flat):
        
        df = join_data(time = time,
                      month = n + 1, 
                      direction = direction)
        
        plotScatter(ax, df)
        
        
    fig.text(0.08, 0.45, "DRIFT", rotation = "vertical", 
             fontsize = 20)
    
    fig.text(0.5, 0.08, "FPI", rotation = "horizontal", 
             fontsize = 20)
    
    fig.suptitle(f"{direction} - {time}")
    
direction = "Zonal"
time = dt.time(0, 0, 0)
#plot_scatter_corr()


observed = 

