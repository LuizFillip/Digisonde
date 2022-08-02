# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 15:32:32 2022

@author: Luiz
"""

import config
#import matplotlib.pyplot as plt
import os
from pipeline import *
import matplotlib.dates as dates
import astral 
import datetime
from astral.sun import sun
import pandas as pd







def plotAnnualvariation(infile, 
                        filename, 
                        site = "Fortaleza", 
                        fontsize = 14,
                        average = False, 
                        save = False):
    
    fig, ax = plt.subplots(figsize = (12, 6))
    
    
    df = sel_parameter(infile, filename, 
                       factor = "peak")
   

      
    date = df.index[0]
    
    args = dict(linestyle = "none", 
                marker = "o", 
                fillstyle = 'none')
    
    ax.plot(df, **args)

    ax.legend(list(df.columns),
              title = "Frequencies (MHz)", 
              loc = 'lower left', 
              prop={'size': fontsize - 2}, 
              ncol = 3)
    
    ax.set(ylabel = ("Velocity (m/s)"), 
           xlabel = ("Months"), 
           ylim = [0, 90])
        
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    
    path_out = f"Figures/{site}/{date.year}/Variations/"
    FigureName = f"prereversalEnhancement_{site}_{date.year}"
    
    if save:
        plt.savefig(f"{path_out}{FigureName}.png", 
                    dpi = 300, bbox_inches="tight")
 

site = "Fortaleza"
infile = f"Results/{site}/PRE/"
filename = "2014.txt"

plotAnnualvariation(infile, 
                        filename, 
                        site = site, 
                        average = True, 
                        save = False)




