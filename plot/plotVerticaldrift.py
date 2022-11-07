import matplotlib.pyplot as plt
#from prereversalEnhancement import PRE, get_values
import datetime
#from plotConfig import *
from digisonde_utils import terminators
from sites import infos_from_filename
from pipeline import iono_frame, drift
import numpy as np
import os


"""

def text_peaks(infile, filename, day):
    peak, time = get_values(infile, filename, day)
    
    peak = np.append(peak, round(vz.Avg.max(), 3))
    time = np.append(time, vz.Avg.idxmax())

    for num in range(len(peak)):
        ax[1].axvline(time[num], linestyle = "-", 
                      lw = 0.5, color = colors[num])
        
        info_text = f"{freqs[num]} MHz: {peak[num]} m/s"
        
        ax[1].text(18.1, 28 + (num*16), info_text, 
                   color = colors[num],
                   transform = ax[1].transData)
"""

def secondary_axis(ax, delta = - 3):
    ax1 = ax.twiny()
    
    ax1.set(xticks = ax.get_xticks(), 
            xlabel = "Time (LT)", 
            xlim = ax.get_xlim())
    
    ax1.xaxis.set_major_formatter(lambda x, pos: 
                                  f"%d" % (x + delta) + ":00")
    
    ax1.xaxis.set_ticks_position('bottom') 
    ax1.xaxis.set_label_position('bottom') 
    ax1.spines['bottom'].set_position(('outward', 55))

def terminator_lines(ax, filename, year, month, day):
    
    terms = terminators(filename, 
                       date = datetime.date(year, 
                                            month, 
                                            day))
    
    times = [terms.sunset, terms.dusk]
    altitudes = [0, 300]
    linestyle = ["-", "--"]
    kargs = dict(lw = 1, color = "k")
    
    
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
        
        text = f"Terminator \n at {altitudes[num]} km"
            
        ax[1].text(times[num] + 0.1, 70, 
                   text,
                   transform = ax[1].transData)
        

    
  
def plotVerticaldrift(infile, 
                      filename,
                      day = 1, 
                      fontsize = 10):

    fig, ax = plt.subplots(figsize = (15, 10), 
                           nrows = 2, 
                           sharex = True)
    
    plt.style.use('seaborn-talk')
    
    plt.subplots_adjust(hspace = 0)
    name = "Fortaleza"
    df = iono_frame(infile, filename)
    
    df = df.sel_day_in(day = day)
    
    freqs = list(df.columns[1:])
    
    colors = ["red", "black", "blue", "m"]
    
    date = df.index[0]
    year, month, day = date.year, date.month, date.day
    

    
    ax[0].set(ylabel = "Altitude (km)", ylim = [100, 600], 
              title = f'{name}, {date.date()}')
        
    ax[0].xaxis.set_major_formatter(lambda x, pos: 
                                  f"%d" % x + ":00")
        
    
    vz = drift(df)
    
    
    args = dict(fillstyle = "none", 
                lw = 2)
    
    for num, col in enumerate(freqs):
        ax[1].plot(vz.time, vz[col], 
                   color = colors[num], 
                    **args)
        ax[0].plot(df.time, df[col], 
                   color = colors[num], 
                    **args)
    
    ax[1].set(xlabel = "Time (UT)", 
              ylabel = "Velocity (m/s)", 
              ylim = [-50, 50], 
              xlim = [18, 24])
    
    ax[0].legend(freqs, loc = 'upper left', 
                 title = "Frequencies (MHz)", 
                 ncol = 3)
    
    # Adding an secundary axes
    secondary_axis(ax[1], delta = - 3)
    
    #Plot terminator solar from date input
    terminator_lines(ax, filename, year, month, day)
    
    
    
    
    return fig

def main():
    
    infile = "database/process/"

    _, _, files = next(os.walk(infile))

    filename = files[0]

    fig = plotVerticaldrift(infile, 
                            filename, 
                            day = 1)

main()