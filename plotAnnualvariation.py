# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 15:32:32 2022

@author: Luiz
"""

import matplotlib.pyplot as plt
import os
from pipeline import *
import matplotlib.dates as dates
import astral 
import datetime
from astral.sun import sun
import pandas as pd

def time_table(filename, 
               latitude = -3.9,
               longitude = -38.58):
    
    observer = astral.Observer(latitude = latitude, 
                               longitude = longitude)
    
    
    
    df = select_parameter(filename).time()
    
    dates = pd.date_range(df.index[0], 
                          df.index[-1], 
                         )
    
    sunset_dusk = []
    for date in dates:
    
        infos = sun(observer, date, 
                dawn_dusk_depression = 18)
        
        
        def time2num(elem):
            
            time = [int(num) for num in elem.split(":")[:2]]
            return round(time[0] + (time[1] /60), 2)
            
        sunset = time2num(str(infos["sunset"].time()))
        dusk = time2num(str(infos["dusk"].time()))
        
        sunset_dusk.append(list((sunset, dusk)))
        
        
    
    return pd.DataFrame(sunset_dusk, 
                        columns=["sunset", "dusk"], 
                        index = dates).resample("10D").asfreq().interpolate()



def plot_indicators(ax):
    df = pd.read_csv("Kp_ap_Ap_SN_F107_since_1932.txt", 
                     header = 39, delim_whitespace=(True))
    df.index  = pd.to_datetime(dict(year = df['#YYY'], 
                                    month = df['MM'], day = df['DD']))
    parameter = "Kp8"
    df = df.loc[(df["#YYY"]  == 2014) & (df[parameter] > 4), [parameter]]
    
    ax1 = ax.twinx()
    df.plot(ax = ax1, marker = "o", linestyle ="none")

def annual_variation(filename, 
                     site = "Fortaleza", 
                     fontsize = 14,
                     average = False, 
                     parameter = "vel",
                     save = False):
    
    fig, ax = plt.subplots(figsize = (12, 6))
    
    if parameter == "vel":
        df = select_parameter(filename).peak()
        ylabel = "Velocity (m/s)"
        ylim  = [0, 90]
    else:
        df = select_parameter(filename).time()
        ylabel = "Time (UT)"
        
        ylim  = [20, 23]
        
        df_time = time_table(filename)
        
        p = ax.plot(df_time, lw = 3)
        name = ["sunset", "dusk"]
        y = [20.4, 21.6]
        
        for num in range(len(p)):
            ax.text(df.index[-12], y[num], 
                    name[num],
                    fontsize = fontsize + 4,
                    color = p[num].get_color(), 
                    transform = ax.transData)
       
    parameter = ylabel.split(" ")[0]
    
    
    date = df.index[0]
    
    args = dict(linestyle = "none", 
                marker = "o", 
                fillstyle = 'none')
    
    df.plot(ax = ax, **args)
    
    ax.legend(title = "Frequencies (MHz)", 
              loc = 'lower left', 
              prop={'size': fontsize - 2}, 
              ncol = 3)
    
    

    ax.set(ylabel = (ylabel), 
           xlabel = ("Months"), 
           ylim = ylim,
           title = "Annual variation of vertical" \
               f"drift in {site} - {date.year}")
        
    #if parameter != "vel":
        

    ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    
    if average:
    
        window = 15
        avg = df.mean(axis = 1).resample(f"{window}D").asfreq().interpolate()
        std = df.std(axis = 1).resample(f"{window}D").asfreq().interpolate()

        ax.errorbar(x = avg.index, 
                    y = avg, 
                    yerr = std,
                    color = "k", 
                    marker = "o", 
                    linestyle = "none")
   
    fig.autofmt_xdate(rotation = 0, ha = 'center')
    
    plt.rcParams.update({'font.size': fontsize, 
                         "font.family": "Times New Roman"})   
    
    
    path_out = f"Figures/{site}/{date.year}/Variations/"
    FigureName = f"AnnualVariation_{parameter}_{site}{date.year}"
    
    if save:
        plt.savefig(f"{path_out}{FigureName}.png", 
                    dpi = 300, bbox_inches="tight")
 


def main():
    filename = "Saoluis2014.txt"
    
    df = select_parameter(filename).peak()
    
    print(df)
    
    #for par in ["time", "vel"]:
 
filename = "Saoluis2014.txt"        
 
annual_variation(filename, site = "SaoLuis", 
                         parameter = "time", save = True)





