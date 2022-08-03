# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 17:44:22 2022

@author: Luiz
"""

import pandas as pd
import config
import numpy as np
import datetime
infile = "Database/PlanetaryIndicators/"
filename = "Kp.txt"


def plot_indicators(infile, ax):
    df = pd.read_csv(infile, 
                     header = 39, delim_whitespace=(True))
    df.index  = pd.to_datetime(dict(year = df['#YYY'], 
                                    month = df['MM'], day = df['DD']))
    parameter = "Kp8"
    df = df.loc[(df["#YYY"]  == 2014) & (df[parameter] > 4), [parameter]]
    
    ax1 = ax.twinx()
    df.plot(ax = ax1, marker = "o", linestyle ="none")
    
    
#df = pd.read_csv(infile, delim_whitespace=(True))
with open(infile + filename) as f:
    data = [line.strip() for line in f.readlines()]
    
header = data[0]



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

outside = []
for num in range(1, len(data)):
    contents = data[num]

    outside.append(row(contents))
    
df = pd.DataFrame(outside)

print(df)