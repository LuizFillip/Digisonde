import os
import pandas as pd
import setup as p 
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
from core import find_header, time_to_float

infile = "database/QF/"
_, _, files = next(os.walk(infile))

filename = files[0]

def build_dataframe(infile, filename):
    """Read QF observations"""
    with open(infile + filename) as f:
       data = [line.strip() for line in f.readlines()]
    
    good_indices = [0, 2, 3]
    
    extract_from_loop  = []
    
    for elem in data:
        
        list_a = elem.split()
        
        if len(list_a) >= 5:
            extract_from_loop.append([list_a[index] for 
                                 index in good_indices])
                        
    df = pd.DataFrame(extract_from_loop, 
                      columns = ["date", "time", "qf"])
    
    df.index = pd.to_datetime(df["date"] +" " + df["time"])
    
    df["qf"] = pd.to_numeric(df["qf"])
    
    return df.loc[:, ["qf"]]


def read_all_files(infile):    
    """Use os library for read all files"""
    _, _, files = next(os.walk(infile))
    
    outside = []
    
    for filename in files:
  
        outside.append(build_dataframe(infile, filename))
        
    return pd.concat(outside)



def plotESFaverage(infile, ax = None):
    
    df = read_all_files(infile)

    df["day"] = df.index.date
    df["time"] = df.index.time

    df["time"] = df["time"].apply(lambda x: time_to_float(x))

    tvalues = df.time.values
    
    df["time"]= np.where((tvalues > 10), 
                  tvalues, tvalues + 24)
    
    
    df = df.loc[(df.time >= 20) & (df.time <= 35), :]


    df = df.loc[~(df.qf > 50), :]
    
    pivot = pd.pivot_table(df, 
                           values = "qf", 
                           index = "time", columns= "day")
    
    if ax == None:
        fig, ax = plt.subplots(figsize = (12, 4))
    
    x = pivot.columns.values
    y = pivot.index.values
    Z = pivot.values
    
    X, Y = np.meshgrid(x, y)
    img = ax.pcolormesh(X, Y, Z, cmap = "coolwarm")
    
    ax.set(ylabel = "Time (UT)")
    
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    ax1 = ax.twinx()
    pivot.mean().plot(ax = ax1, lw = 1, color = "k")
    
    return img
    
    

#read_all_files(infile)
#plotESFaverage(infile, ax = None)



