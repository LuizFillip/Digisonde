# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 18:06:16 2022

@author: Luiz
"""
import os
import pandas as pd
import config
from ionosonde import *
import matplotlib.pyplot as plt
import matplotlib.dates as dates



infile = "Database/QF/"

def read_all_files(infile):
    _, _, files = next(os.walk(infile))
    
    outside = []
    
    for filename in files:
        df = pd.read_csv(infile + filename, 
                         header = 5, 
                         delim_whitespace=(True), 
                         index_col=(False),
                         names = ["date","doy", "time", "qf"])
        
        df.index = pd.to_datetime(df["date"] +" " + df["time"])
    
        outside.append(df.loc[:, ["qf"]])
        
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
    
    

read_all_files(infile)
#plotESFaverage(infile, ax = None)