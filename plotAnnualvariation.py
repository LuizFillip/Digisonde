# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 15:32:32 2022

@author: Luiz
"""

import matplotlib.pyplot as plt
import os
from pipeline import *
import matplotlib.dates as dates
from scipy.signal import savgol_filter
save = False

filename = "Fortaleza2014.2.txt"

df = select_parameter(filename).peak()

avg = df.mean(axis = 1).resample('3D').last().interpolate()

# 

savgol_data = savgol_filter(avg.values, window_length= 21, polyorder = 1)



df1 = pd.DataFrame(savgol_data, 
                   index = avg.index).resample("M").last()



fig, ax = plt.subplots(figsize = (12, 6))

args = dict(linestyle = "none", 
            marker = "o", 
            fillstyle = 'none')

df.plot(ax = ax, **args)

ax.legend( 
          title = "Frequencies (MHz)", ncol = 1)


ax.plot(avg.index, savgol_data, color = "k", lw = 2)

ax.text(0.8, 0.1, " - Filtered average", transform = ax.transAxes)
ax.set(ylabel = ("Velocity (m/s)"), 
       xlabel = ("Months"), 
       title = "Annual variation of vertical drift in Fortaleza - 2014")


ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))

fig.autofmt_xdate(rotation=0, ha = 'center')

plt.rcParams.update({'font.size': 14})   
plt.rcParams["font.family"] = "Times New Roman"


path_out = "Figures/Fortaleza/2014/Variations/"
FigureName = "VerticalDrift2014"

if save:
    plt.savefig(f"{path_out}{FigureName}.png", 
                dpi = 100, bbox_inches="tight")

   

plt.show()

