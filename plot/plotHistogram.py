# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 18:39:48 2022

@author: Luiz
"""

import matplotlib.pyplot as plt
import os
from pipeline import *
import config

def plotHistogram(infile,
                  filename, 
                  fontsize = 18,
                  parameter = "peak",
                  save = False, 
                  site = "Fortaleza",
                  xlabel = 'Velocity', 
                  unit = "m/s", 
                  binwidth = 5, 
                  ncols = 3, 
                  year = 2014):
    
   
        
    df = sel_parameter(infile, filename, 
                       factor = parameter)
    
    
    max_value = round(df.max().max())
    min_value = round(df.min().min())
 
    bins = np.arange(min_value, 
                     max_value + binwidth, 
                     binwidth)
    
    columns = df.columns
    
    fig, ax = plt.subplots(figsize = (18, 4), 
                           ncols = ncols, 
                           nrows = len(columns) // ncols, 
                           sharex = True, 
                           sharey = True)

    plt.subplots_adjust(hspace = 0.2, wspace = 0.)
    
    args = dict(facecolor = 'lightgrey', 
                alpha = 1, 
                edgecolor = 'black', 
                hatch = '////', 
                color = 'gray', 
                linewidth = 1)
    
    
    
    for col, ax in zip(columns, ax.flat):
    
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

    fig.text(0.5, 0., f"{xlabel} ({unit})", 
             va = 'bottom', 
             ha='center', 
             fontsize = fontsize)
    
    fig.text(0.08, 0.5, 'Number of events', 
             va='center', 
             rotation='vertical', 
             fontsize = fontsize + 2)   
    
    fig.suptitle(f'Vertical drift in {site} - {year}', 
                 size = fontsize + 2, y= 1.1)
    
   
    #path_out = f"Figures/{site.strip()}/{year}/Histograms/"
    path_out = "img/"
    FigureName =  "histogram" #xlabel.capitalize()
    
    if save:
        plt.savefig(f"{path_out}{FigureName}.png", 
                    dpi = 200, bbox_inches="tight")
    
    plt.show()
    
    
def main():
    infile = "Results/Fortaleza/PRE/"
    filename = "2014.txt"
    site = "Fortaleza"
    year = int(filename.replace(".txt", ""))
    plotHistogram(infile, 
                  filename, 
                  year = year,
                  site = site, 
                  parameter = "peak", 
                  binwidth = 8,
                  save = True)
    
    
    
main()
