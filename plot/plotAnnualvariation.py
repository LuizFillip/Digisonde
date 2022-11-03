from plotConfig import *
import matplotlib.pyplot as plt
import os
from pipeline import *
import matplotlib.dates as dates
import pandas as pd


def plotAnnualvariation(infile, 
                        filename, 
                        site = "Fortaleza", 
                        fontsize = 14,
                        average = False, 
                        save = False, 
                        ax = None):
    if ax == None:
        fig, ax = plt.subplots(figsize = (10, 5))
    
    
    df = sel_parameter(infile, filename, 
                       factor = "peak")
   
    date = df.index[0]
    
    markers = ["o", "^", "s"]
    colors = ['#FF2C00', '#845B97', '#00B945']
    
    ax.plot(df.index, df.mean(axis = 1), marker = "o", 
            linestyle = "none", color = "k", markersize = 5)
    


    ax.legend(list(df.columns),
              title = "Frequencies (MHz)", 
              loc = 'upper center', 
              prop={'size': fontsize - 2}, 
              ncol = 3)
    
    ax.set(ylabel = ("Velocity (m/s)"), 
           xlabel = ("Months"), 
           ylim = [0, 90])
        
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    
  
 

def plotAnnualAvg():
    year = 2014
    site = "Fortaleza"
    infile = f"process/{site}/PRE/"
    
    filename = f"{year}.txt"
    
    out = []
    for pe in ["time", "peak"]:
        
    
        out.append(sel_parameter(infile, filename, 
                       factor = pe).mean(axis = 1))
        
    df = pd.concat(out, axis = 1)
    
    df.columns = ["time", "peak"]
    
    fig, ax = plt.subplots(figsize = (14, 7))
    
    df["peak"].plot(marker = "o", 
                    linestyle = "none", 
                    markersize = 10,
                    fillstyle = "none",
                    color = "k")
    
    ax.set(ylabel = "Velocidade (m/s)", 
           xlabel = "Meses", 
           ylim = [0, 90])
    
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    ax.tick_params(axis = 'x', labelrotation = 0)
    
    
    fig.savefig(paths["latex"] + "PRE_annual_2014.png", 
                dpi = 1000, 
                bbox_inches = "tight")
     
    #df.to_csv(f"{year}.txt", index = True, sep = ",")

main()