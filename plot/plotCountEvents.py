import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import setup as s
import os



def plot(ax, infile, filename):
    args = filename.split("_")
        
    df = pd.read_csv(infile + filename, 
                     index_col = 0)
    ymin = min(df.index)
    ymax = max(df.index)
    img = ax.pcolormesh( df.columns, 
                        df.index,
                        df.values, 
                        cmap = "Blues", 
                        vmax = 144)
                    
    ax.set_xticks(np.arange(0, 365, 30))
    
    years = np.arange(ymin, ymax)
    
    ax.set_yticks(years + 0.5, (years), va = "center")
    
    ax.set(ylabel = "Anos", 
           xlabel = "Dias", 
           ylim = [ymin - 0.5, ymax - 0.5])
    
    ax.text(0., 1.08,  f"{args[0]}", 
            transform = ax.transAxes, 
            fontsize = 16)
    
    s.colorbar_setting(img, ax, 
                       ticks = np.arange(0, 150, 20),
                       label = "# dados por dia")
    return ax
   

fig, axes = plt.subplots(nrows = 2, 
                       figsize = (10, 7), 
                       sharex = True)

s.config_labels()
 
 
infile = "database/counts/"

_, _, files = next(os.walk(infile))

for num, a in enumerate(axes.flat):
    ax = plot(a, infile, files[num])
    if num == 0:
        ax.set(xlabel = "")
    
plt.show()