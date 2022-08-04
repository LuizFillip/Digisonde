# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 11:45:16 2022

@author: Luiz
"""

import pandas as pd
import config
import numpy as np
import datetime


def row(contents):
    result = []
    
    date = contents[:8]
    kptimes = contents[9:25]
    sumkp = contents[25:28]
    aptimes = contents[28:52]
    Ap = contents[52:55] 
    
    kptimes_ = [kptimes[num: num + 2].strip() 
                for num in range(0, len(kptimes), 1) 
                if (num % 2) == 0]
    
    def _str_to_date(string_date):
        
        year = int(string_date[:4])
        month = int(string_date[4:6])
        day = int(string_date[6:8])
        
        return datetime.date(year, month, day)
    
    aptimes_ = [int(num.strip()) for num in aptimes.split()]
    
    result.append(_str_to_date(date))
    result.extend(kptimes_)
    result.append(sumkp)
    result.extend(aptimes_)
    result.append(int(Ap.strip()))

    return (result)

def plotKyotoData():
    
    infile = "Database/PlanetaryIndicators/"
    filename = "Kp.txt"
    
    
    with open(infile + filename) as f:
        data = [line.strip() for line in f.readlines()]
        
    
    
    outside = []
    
    for num in range(1, len(data)):
        contents = data[num]
    
        outside.append(row(contents))
        
    
    col_names = ["date", 'kp0', 'kp3', 
                 'kp6', 'kp9', 'kp12', 
                 'kp15', 'kp18', 'kp21',
                 'kpsum', 'ap3', 'ap6', 
                 'ap9', 'ap12', 'ap15', 
                 'ap18', 'ap21', 'ap24', "Ap"]
    
    df = pd.DataFrame(outside, columns = col_names)
    
    df.index = pd.to_datetime(df["date"])
    
    df = df.loc[df.index.year == 2014, :]
    return df

def plotKp(infile, filename, 
            parameter = "Ap", 
            year = 2014, 
            ax = None):
    
    
    df = pd.read_csv(infile + filename, 
                     header = 39, delim_whitespace=(True))
    
    
    df.index  = pd.to_datetime(dict(year = df['#YYY'], 
                                    month = df['MM'], 
                                    day = df['DD']))
    
    df = df.loc[(df["#YYY"]  == year), [parameter]]
    
    ax.plot(df, lw = 1, color = "gray")
    
    ax.set(ylabel = "Ap index", xlabel = "Months")
    
    ax.axhline(22, color = "k", 
               linestyle = "--", label = "Ap = 22 (kp = 4)")
    
    ax.legend(loc = "upper right")
    
 