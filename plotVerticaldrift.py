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



def plot(iono, day, 
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
                 title = "Frequencies (MHz)", ncol = 6)
    
    # =============================================================================
    # TERMINATOR SOLAR AT 300 KM 
    # =============================================================================
    year, month, day = date.year, date.month, date.day
    
    observer = astral.Observer(latitude = -3.9, longitude = -38.58)
    date = datetime.date(year, month, day)
    infos = sun(observer, date, dawn_dusk_depression=18)

    
  
    
    # minor and major axis formater (date and time) 
    import matplotlib.dates as dates
    
    ax[1].xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    ax[1].xaxis.set_major_locator(dates.HourLocator(interval = 1))
    
    ax2 = ax[1].twiny()
    data = np.empty(len(drift))
    data[:] = np.nan
    index = pd.to_datetime(drift.index + pd.Timedelta(hours = -3))
    
    xs = pd.Series(data= data,
                   index = index)
    
    xs.plot(ax = ax2)
    
    ax2.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    ax2.xaxis.set_major_locator(dates.HourLocator(interval = 1))
 
   
    ax2.xaxis.set_ticks_position('bottom') 
    ax2.xaxis.set_label_position('bottom') 
    ax2.spines['bottom'].set_position(('outward', 45))
    
    
    
    ax2.set(xlabel = "Time (LT)")
    
    


    plt.rcParams.update({'font.size': 12, 
                         "font.family": "Times New Roman", 
                         })   
  
    angles = ["sunset", "dusk"]
    linestyle = ["-", "--"]
    for num in range(2):
        
        terminator = infos[angles[num]]
        
        ax[0].axvline(
            terminator, color = "k", linestyle = linestyle[num], 
                        )
        
        ax[0].axvline(
            terminator, color = "k", linestyle = linestyle[num], 
                        )
        
        delta = datetime.timedelta(minutes = 5)
        
        if angles[]
        ax[1].text(terminator + delta,110, 
                   "Solar terminator \nat 300 km",
                   transform=ax[1].transData)
    
# =============================================================================
#     SAVE
# =============================================================================
    
    doy = date.timetuple().tm_yday
    
    if doy < 10:
        FigureName = f"00{doy}"
        
    elif doy > 10 and doy < 100:
        FigureName = f"0{doy}"

    else:
        FigureName = f"{doy}"
    
    
    
    path_out = "Figures/Fortaleza/2014/"
    
    if save:
        plt.savefig(f"{FigureName}.png", 
                    dpi = 100, bbox_inches="tight")
    
        plt.close(fig)
  
        
def main():
    infile = "Database/FZ_2014-2015_Processado/"
    
    _, _, files = next(os.walk(infile))
    
    filename = files[11]
    
    
    iono = ionosonde(infile, filename)
    #PRE(df)    #for day in range(1, 31, 1):
        
    plot(iono, 31, save = False)
    
main()