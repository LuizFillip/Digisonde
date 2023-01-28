import pandas as pd
import matplotlib.pyplot as plt
import os
from utils import smooth
import numpy as np

def load(infile):

    df = pd.read_csv(infile, 
                     delim_whitespace = True, 
                     header = None)
    
    df.index = pd.to_datetime(df[6] + " " + df[8])
    df.drop(columns = list(range(9)) + list(range(19, 24)), 
            inplace = True)
    
    return df

def load_all_day(infile):
    
    _, _, files = next(os.walk(infile))

    files = [f for f in files if f.endswith("DVL")]

    out = [load(infile + f) for f in files]
    
    return pd.concat(out)

def plotAll(df):

    fig, ax = plt.subplots(nrows = 5, 
                           figsize = (8, 10), 
                           sharex = True)
    
    plt.subplots_adjust(hspace = 0)
    
    labels = ["Vx", "Vy", "Az", "Vh", "Vz"]
    
    
    for num, col in enumerate(df.columns[::2]):
        df[col].plot(ax = ax[num], 
                     marker = "o", 
                     markersize = 3,
                     yerr = df[col + 1])
        ax[num].axhline(0, color = "k")
        l = labels[num]
        ax[num].set(ylabel = f"{l} (m/s)")
        
        

def get_pre(infile):
    df = load_all_day(infile)
    pre = df.loc[(df.index.hour >= 18), 17]
    x = pre.index
    y = pre.values
    vzp = np.max(smooth(y, 3))
    tzp = x[np.argmax(y)]
    return tzp, vzp

def main():
    infile = "C:\\2013001\\"
    
    
    
    time, vzp = get_pre(infile)
    
    out = {"time": [], 
           "vzp": []}
    
    print(time, vzp)
    
    
    


