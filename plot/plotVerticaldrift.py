import matplotlib.pyplot as plt
from PRE import drift
import datetime
from plotConfig import path_tex
from digisonde_utils import terminators
from pipeline import iono_frame
import numpy as np
import os



def secondary_axis(ax, delta = - 3):
    ax1 = ax.twiny()
    
    ax1.set(xticks = ax.get_xticks(), 
            xlabel = "Hora (LT)", 
            xlim = ax.get_xlim())
    
    ax1.xaxis.set_major_formatter(lambda x, pos: 
                                  "%d" % (x + delta) + ":00")
    
    ax1.xaxis.set_ticks_position('bottom') 
    ax1.xaxis.set_label_position('bottom') 
    ax1.spines['bottom'].set_position(('outward', 110))

def terminator_lines(ax, filename, year, month, day):
    
    terms = terminators(filename, 
                       date = datetime.date(year, 
                                            month, 
                                            day))
    
    times = [terms.sunset, terms.dusk]
    altitudes = [0, 300]
    linestyle = ["-", "--"]
    kargs = dict(lw = 2, color = "k")
    
    letter = ["(a)", "(b)"]
    for num in range(2):
            
        for col in range(2):
        
            ax[col].axvline(
                    times[num], 
                    linestyle = linestyle[num], 
                    **kargs)
            
            ax[col].axvline(
                    times[num], 
                    linestyle = linestyle[num], 
                    **kargs)
        
        text = f"Terminadouro \n em {altitudes[num]} km"
            
        ax[0].text(times[num] + 0.1, 210, 
                   text, 
                   transform = ax[0].transData)
        
        
        ax[num].text(0.02, 0.9, 
                     letter[num], 
                     transform = ax[num].transAxes)
        

def shading(ax, start = 22.10, end = 24.0):

    ax.axvspan(start, end, alpha = 0.5, color = "gray")
    ax.text(start + 0.7, 30, "ESF", transform = ax.transData)
  
def plotVerticaldrift(infile, 
                      filename,
                      day = 1, 
                      name = "Fortaleza"):

    fig, ax = plt.subplots(figsize = (25, 20), 
                           nrows = 2, 
                           sharex = True)
    
    
    plt.subplots_adjust(hspace = 0.1)
    
    df = iono_frame(infile, filename)
    
    df = df.sel_day_in(day = day)
    
    freqs = list(df.columns[1:])
    
  
    date = df.index[0]
    year, month, day = date.year, date.month, date.day
    

    
    ax[0].set(ylabel = "Altitude (km)", 
              ylim = [200, 400], 
              )
        
    ax[0].xaxis.set_major_formatter(lambda x, pos: "%d" % x + ":00")
        
    vz = drift(df)
    
    
    shading(ax[1], start = 22.10, end = 24.0)
    args = dict(fillstyle = "none", 
                lw = 3)
    
    for num, col in enumerate(freqs):
        ax[1].plot(vz.time, vz[col],
                    **args)
        ax[0].plot(df.time, df[col], 
                    **args)
    ax[1].set(xlabel = "Hora (UT)", 
              ylabel = r"$V_z$ (m/s)", 
              ylim = [-50, 50], 
              yticks = np.arange(-40, 45, 10),
              xlim = [18, 24])
    
    ax[0].legend(freqs, 
                 loc = 'lower left',
                 title = "Frequências (MHz)", 
                 ncol = 3)
    
    secondary_axis(ax[1], delta = - 3)
    terminator_lines(ax, filename, year, month, day)
    date_str = date.strftime("%d de %B de 2014")
    fig.suptitle(f'{name}, {date_str}', y = 0.91)
   
    return fig

def main():
    
    infile = "database/process/"

    _, _, files = next(os.walk(infile))

    filename = files[0]
    

    fig = plotVerticaldrift(infile, 
                            filename, 
                            day = 1)

    fig.savefig(path_tex["latex"] + "vz_and_heights.png", 
               dpi = 500)

main()