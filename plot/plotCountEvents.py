import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import setup as s
import os

infile = "database/counts/"


_, _, files = next(os.walk(infile))

filename = files[1]


def plot(infile, filename):
    args = filename.split("_")
    ystart = int(args[1])
    yend = int(args[-1].replace(".txt", ""))
    
    fig, ax = plt.subplots(figsize = (10, 4))
    
    s.config_labels()
    
    df = pd.read_csv(infile + filename, index_col = 0)
    
    img = ax.pcolormesh(df.columns, 
                        df.index, 
                        df.values, 
                        cmap = "Blues", 
                        vmax = 144)
    
    ax.set_xticks(np.arange(0, 365, 30))
    
    
    ax.set(ylabel = "Anos", 
           xlabel = "Dias", 
           yticks = list(df.index),
           ylim = [ystart, yend],
           title = f"Velocidade de deriva - {args[0]}")
    
    s.colorbar_setting(img, ax, 
                       ticks = np.arange(0, 150, 20),
                       label = "# dados por dia")
    
    plt.show()
