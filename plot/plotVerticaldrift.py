import matplotlib.pyplot as plt
from prereversalEnhancement import PRE, drift
import datetime
import matplotlib.ticker as ticker
import plotConfig
from digisonde_utils import terminators
from sites import coords_from_filename
from pipeline import select_day
import unicodedata
import numpy as np





def secondary_axis(ax, delta = - 3):
    ax1 = ax.twiny()
    
    ax1.set(xticks = ax.get_xticks(), 
            xlabel = "Time (LT)", 
            xlim = ax.get_xlim())
    
    ax1.xaxis.set_major_formatter(lambda x, pos: 
                                  f"%d" % (x + delta) + ":00")
    
    ax1.xaxis.set_ticks_position('bottom') 
    ax1.xaxis.set_label_position('bottom') 
    ax1.spines['bottom'].set_position(('outward', 45))

def terminator_lines(ax, filename, fontsize, year, month, day):
    
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
            
        ax[1].text(times[num] + 0.1, 110, 
                   text,
                   transform = ax[1].transData, 
                   fontsize = fontsize)
        

    
  
def plotVerticaldrift(infile, 
                      filename,
                      day = 1, 
                      fontsize = 14,
                      save = True):
    
    if save: 
        plt.ioff()

    fig, ax = plt.subplots(figsize = (10, 6), 
                           nrows = 2, sharex = True)
    
    plt.style.use('seaborn-talk')
    
    plt.subplots_adjust(hspace = 0)
    
    name, lat, lon = coords_from_filename(filename)
    df = select_day(infile, filename, day)
    
    df["Avg"] = df[[6, 7, 8]].mean(axis = 1)
    

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
                lw = 1)
    
    for num, col in enumerate(freqs):
        ax[1].plot(vz.time, vz[col], 
                   color = colors[num], 
                    **args)
        ax[0].plot(df.time, df[col], 
                   color = colors[num], 
                    **args)
    
    ax[1].set(xlabel = "Time (UT)", 
              ylabel = "Velocity (m/s)", 
              ylim = [-90, 90], 
              xlim = [18, 24])
    
    ax[0].legend(freqs, loc = 'upper left', 
                 prop={'size': fontsize - 2},
                 title = "Frequencies (MHz)", 
                 ncol = 3)
    
    # Adding an secundary axes
    secondary_axis(ax[1], delta = - 3)
    
    #Plot terminator solar from date input
    terminator_lines(ax, filename, fontsize, year, month, day)
    
    
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
    
    site_to_save = unidecode(name).replace(" ", "")
    FigureName = date.strftime("%j")
    
    if save:
        
        path_out = f"Figures//{site_to_save}//{date.year}//IndividualsPlots//"
        
        try:
            plt.savefig(f"{path_out}{FigureName}.png", 
                    dpi = 100, bbox_inches = "tight")
        except:
            plt.savefig(f"{FigureName}.png", 
                    dpi = 100, bbox_inches = "tight")
    
        plt.close(fig)
  

def main():
    
    infile = "Database/FZ_2014-2015_Processado/"
     
    _, _, files = next(os.walk(infile))
     
    filename = files[11]
    plotVerticaldrift(infile, filename, 
                      day = 2, save = False)

main()