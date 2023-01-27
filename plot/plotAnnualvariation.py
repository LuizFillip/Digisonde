import setup as p

import matplotlib.pyplot as plt
import os
import matplotlib.dates as dates
import pandas as pd
 
def tex_path(folder):
    
    latex = "G:\\My Drive\\Doutorado\\Modelos_Latex_INPE\\docs\\Proposal\\Figures\\"
    return os.path.join(latex, folder)


def plotAnnualAvg(infile = "database/FZ_PRE_2014_2015.txt", 
                  year = 2014):
    
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    df = df.loc[df.index.year == year]
    
    avg = df.resample("15D").mean()
    
    fig, ax = plt.subplots(figsize = (10, 5))
    p.config_labels()
    
    df["vz"].plot(marker = "o", 
                    markersize = 5,
                    linestyle = "none",
                    color = "red")
    
    ax.set(ylabel = "$V_{zp}$ (m/s)", 
           xlabel = "Meses", 
           ylim = [0, 90])
    
    
    ax.plot(avg["vz"], color = "k", lw = 3, 
            label = "Média (15 dias)")
    
    ax.text(0.01, 0.9, year, transform = ax.transAxes)
    
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    ax.tick_params(axis = 'x', labelrotation = 0)
    
    return fig
     
def main():

    plotAnnualAvg()
    
    #name = tex_path("results\\PRE_annual_2014.png")
    #fig.savefig(name)
    
main()