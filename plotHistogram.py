# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 18:39:48 2022

@author: Luiz
"""

from ionosonde import *
import matplotlib.pyplot as plt
import os
from pipeline import *


def plotHistogram(
                  filename, 
                  fontsize = 18,
                  parameter = "vel",
                  save = False, 
                  site = "Fortaleza",
                  ):
    
    if parameter == "vel":
        
        df = select_parameter(filename).peak()
        
        binwidth = 5
        xlabel = 'Velocity'
        unit = "m/s"
    else:
        df = select_parameter(filename).time()
        binwidth = 0.3
        xlabel = "Time"
        unit = "UT"
    
    year = df.index[0].year
    
    max_value = round(df.max().max())
    min_value = round(df.min().min())
 
    bins = np.arange(min_value, 
                     max_value + binwidth, 
                     binwidth)

    fig, ax = plt.subplots(figsize = (18, 8), 
                           ncols = 3, nrows = 2, 
                           sharex = True, 
                           sharey = True)

    plt.subplots_adjust(hspace = 0.2, wspace = 0.)
    
    args = dict(facecolor = 'lightgrey', alpha = 1, 
                edgecolor = 'black', hatch = '////', 
                color = 'gray', linewidth = 1)
    
    
    
    for col, ax in zip(df.columns, ax.flat):
    
        df[col].hist(bins = bins, 
                       ax = ax, **args)
        
        mean = round(df[col].mean(), 2)
        std = round(df[col].std(), 2)
        
        infos = f"$<V_z> = {mean}$ {unit} \n $\sigma = {std}$ {unit}"
        
        ax.text(0.6, 0.7, infos, 
                fontsize = fontsize - 4, 
                transform = ax.transAxes)
        
        ax.set(title = f"Frequency - {col} MHz", 
               xlim = [min_value - binwidth, 
                       max_value + binwidth])

    fig.text(0.5, 0.055, f"{xlabel} ({unit})", 
             va = 'bottom', 
             ha='center', 
             fontsize = fontsize)
    
    fig.text(0.09, 0.5, 'Number of events', 
             va='center', 
             rotation='vertical', 
             fontsize = fontsize + 2)   
    
    fig.suptitle(f'Vertical drift in {site} - {year}', 
                 size = fontsize + 4)
    
    plt.rcParams.update({'font.size': fontsize - 2, 
                         "font.family": "Times New Roman"})   
    
    path_out = f"Figures/{site.strip()}/{year}/Histograms/"
    FigureName = xlabel.capitalize()
    
    if save:
        plt.savefig(f"{path_out}{FigureName}.png", 
                    dpi = 300, bbox_inches="tight")
    
    plt.show()
    
    
def main():
    filename = "Saoluis2015.txt"
    
    
    for par in ["time", "vel"]:
        plotHistogram(filename, site = "SaoLuis", 
                  parameter = par, save = True)
main()
