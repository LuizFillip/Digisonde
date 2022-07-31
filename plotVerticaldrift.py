# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 16:12:49 2022

@author: Luiz
"""

import matplotlib.pyplot as plt
from ionosonde import *
from prereversalEnhancement import *
import astral 
import datetime
import matplotlib.ticker as ticker


def get_values(infile, filename, day):
    df = PRE(infile, filename, 
              day = day, delta = 1)
    
    peak = df.iloc[(df.index.get_level_values('Values') == 
                            "peak"), :].values[0]
    
    time = df.iloc[(df.index.get_level_values('Values') == 
                            "time"), :].values[0]

    return (peak, time)


def secundary_axes(ax, delta = - 3):
    ax1 = ax.twiny()
    
    ax1.set(xticks = ax.get_xticks(), 
            xlabel = "Time (LT)", 
            xlim = ax.get_xlim())
    
    ax1.xaxis.set_major_formatter(lambda x, pos: 
                                  f"%d" % (x + delta) + ":00")
    
    for axs in [ax, ax1]:
        
        axs.xaxis.set_major_locator(ticker.AutoLocator())
        axs.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        
        axs.yaxis.set_major_locator(ticker.AutoLocator())
        axs.yaxis.set_minor_locator(ticker.AutoMinorLocator())
        
    
    ax1.xaxis.set_ticks_position('bottom') 
    ax1.xaxis.set_label_position('bottom') 
    ax1.spines['bottom'].set_position(('outward', 45))

def terminator_lines(ax, filename, fontsize, year, month, day):
    
    terms = terminators(filename, 
                       date = datetime.date(year, month, day))
    
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
        
def doy_str_format(date):
    
    doy = date.timetuple().tm_yday
    
    if doy < 10:
        FigureName = f"00{doy}"
        
    elif doy > 10 and doy < 100:
        FigureName = f"0{doy}"

    else:
        FigureName = f"{doy}"
        
    return FigureName
  
    
  
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
    
    # =============================================================================
    # F LAYER HEIGHT     
    # =============================================================================
    
    site_name = sites(filename).name
    df = select_day(infile, filename, day)
    
    freqs = list(df.columns[1:])
    
    colors = ["red", "black", "blue"]
    markers = ["^", "o", "s"]
    
    date = df.index[0]
    year, month, day = date.year, date.month, date.day
    

    
    ax[0].set(ylabel = "Altitude (km)", ylim = [100, 600], 
              title = 'F layer true heights and vertical ' \
                  f'drift (dhF/dt)s in {site_name}, {date.date()}')
        
    ax[0].xaxis.set_major_formatter(lambda x, pos: 
                                  f"%d" % x + ":00")
        
    ax[0].yaxis.set_major_locator(ticker.AutoLocator())
    ax[0].yaxis.set_minor_locator(ticker.AutoMinorLocator())
    
    # =============================================================================
    # VERTICAL DRIFT SUBPLOT
    # =============================================================================
    
    vz = drift(df)
    args = dict(fillstyle = "none", 
                markersize = 3, lw = 1)
    
    for num, col in enumerate(freqs):
        ax[1].plot(vz.time, vz[col], 
                   color = colors[num], 
                   marker = markers[num], **args)
        ax[0].plot(df.time, df[col], 
                   color = colors[num], 
                   marker = markers[num], **args)
    
    ax[1].set(xlabel = "Time (UT)", 
              ylabel = "Velocity (m/s)", 
              ylim = [-90, 90], 
              xlim = [18, 24])
    
    ax[0].legend(freqs, loc = 'upper left', 
                 prop={'size': fontsize - 2},
                 title = "Frequencies (MHz)", 
                 ncol = 3)
    
    
    secundary_axes(ax[1], delta = - 3)
    
    
    # =============================================================================
    # TERMINATOR SOLAR AT 300 KM (DUSK)
    # =============================================================================
    terminator_lines(ax, filename, fontsize, year, month, day)
    
    
    peak, time = get_values(infile, filename, day)
    

    for num in range(len(peak)):
        ax[1].axvline(time[num], linestyle = "-", 
                      lw = 0.5, color = colors[num])
        
        info_text = f"{freqs[num]} MHz: {peak[num]} m/s"
        ax[1].text(18.1, 38 + (num*13), info_text, 
                   color = colors[num],
                   transform = ax[1].transData)
    
    plt.rcParams.update({'font.size': fontsize, 
                         'mathtext.fontset': 'stix', 
                         'font.family': 'STIXGeneral'
                         })   

    site_to_save = unidecode(site_name).replace(" ", "")
    FigureName = doy_str_format(date)
    
    
    if save:
        
        path_out = f"Figures//{site_to_save}//{date.year}//IndividualsPlots//"
        #Figures/Fortaleza/2014/IndividualPlots
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
    
    filename = files[3]
    
    for day in range(1, 32):
        plotVerticaldrift(infile, filename, day = day, save = True)
    

#main()
