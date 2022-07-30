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
from astral.sun import sun
import matplotlib.dates as dates

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

def terminator_lines(ax):
    
    observer = astral.Observer(latitude = latitude, 
                               longitude = longitude)
    
    
    infos = sun(observer, date, 
                dawn_dusk_depression = twilightAngle)
    

    angles = ["sunset", "dusk"]
    linestyle = ["-", "--"]
    for num in range(2):
        
        terminator = infos[angles[num]]
        
        
        for col in range(2):
        
            ax[col].axvline(
                terminator, color = "k", linestyle = linestyle[num], 
                            )
            
            ax[col].axvline(
                terminator, color = "k", linestyle = linestyle[num], 
                            )
        
        delta = datetime.timedelta(minutes = 5)
        
        if angles[num] == "dusk":
            text = "dusk at \n300 km".capitalize()
        else:
            text = angles[num].capitalize()
            
        ax[1].text(terminator + delta, 110, 
                   text,
                   transform = ax[1].transData, 
                   fontsize = fontsize + 2)
def doy_str_format(date):
    
    doy = date.timetuple().tm_yday
    
    if doy < 10:
        FigureName = f"00{doy}"
        
    elif doy > 10 and doy < 100:
        FigureName = f"0{doy}"

    else:
        FigureName = f"{doy}"
        
    return FigureName
  
    
  
def plotVerticaldrift(iono, day, 
                     twilightAngle = 18, 
                     latitude = -3.9,
                     longitude = -38.58,
                     fontsize = 14,
                     site = "Fortaleza",
                     save = True):
    
    if save: 
        plt.ioff()

    fig, ax = plt.subplots(figsize = (10, 8), 
                           nrows = 2, sharex = True)
    
    plt.subplots_adjust(hspace = 0)
    
    # =============================================================================
    # F LAYER HEIGHT     
    # =============================================================================
        
    height = iono.select_day(day)
    date = height.index[0]
    
    ax[0].plot(height, lw = 1)
    
    ax[0].set(ylabel = "Altitude (Km)", ylim = [100, 700], 
              title = 'F layer true heights and vertical ' \
                  f'drift (dhF/dt)s in Fortaleza, {date.date()}')
    
    # =============================================================================
    # VERTICAL DRIFT SUBPLOT
    # =============================================================================
    
    drift = vertical_drift(iono.select_day(day))
        
    ax[1].plot(drift, lw = 1)
    
    ax[1].set(xlabel = "Time (UT)", 
              ylabel = "Velocity (m/s)", 
              ylim = [-90, 90])
    
    ax[1].legend(drift.columns, loc = 'lower left', 
                 prop={'size': fontsize - 2},
                 title = "Frequencies (MHz)", ncol = 3)
    
    
    
    #ax[1].xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    #ax[1].xaxis.set_major_locator(dates.HourLocator(interval = 1))
    
    secundary_axes(ax[1], delta = - 3)
    
    
    # =============================================================================
    # TERMINATOR SOLAR AT 300 KM (DUSK)
    # =============================================================================
    
    
    plt.rcParams.update({'font.size': fontsize, 
                         "font.family": "Times New Roman", 
                         })   

  
    FigureName = doy_str_format(date)
    path_out = f"Figures/{site}/{date.year}/IndividualsPlots/"
    
    if save:
        plt.savefig(f"{path_out}{FigureName}.png", 
                    dpi = 300, bbox_inches = "tight")
    
        plt.close(fig)
  
        
def main():
    infile = "Database/SL_2014-2015_Processado/"
    
    _, _, files = next(os.walk(infile))
    
    filename = files[0]
    
    #print(filename)
    
    
    iono = ionosonde(infile, filename)

        
    plotVerticaldrift(iono, 1, save = False, site = "SaoLuis")
    
main()