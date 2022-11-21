from plotConfig import *
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

import matplotlib.pyplot as plt
import os
from pipeline import *

import matplotlib.dates as dates
import pandas as pd
 
def tex_path(folder):
    
    latex = "G:\\My Drive\\Doutorado\\Modelos_Latex_INPE\\docs\\Proposal\\Figures\\"
    return os.path.join(latex, folder)


def plotAnnualAvg(year = 2014):
    infile = "database/FZ_PRE_2014_2015.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    df = df.loc[df.index.year == year]
    
    fig, ax = plt.subplots(figsize = (25, 10))
    
    df["vz"].plot(marker = "o", 
                    markersize = 15,
                    linestyle = "none",
                    color = "red")
    
    ax.set(ylabel = "$V_{zp}$ (m/s)", 
           xlabel = "Meses", 
           ylim = [0, 90])
    
    ax.text(0.01, 0.9, year, transform = ax.transAxes)
    
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    ax.tick_params(axis = 'x', labelrotation = 0)
    
    name = tex_path("results\\PRE_annual_2014.png")
    fig.savefig(name, dpi = 300)
     
    #df.to_csv(f"{year}.txt", index = True, sep = ",")
plotAnnualAvg()