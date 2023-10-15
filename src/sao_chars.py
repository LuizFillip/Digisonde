import numpy as np
import pandas as pd
import digisonde as dg
import base as b 


def chars(infile):
    f = open(infile).readlines()
    
    raw_data = [f[i].split() for i 
                in range(2, len(f))]
        
    colums = [
        "date", "doy", "time", 
        'foF2', 'hF2', 'QF', 
        'hmF2', 'f(hF)', 'f(hF2)'
        ]
    
    df = pd.DataFrame(
        raw_data, 
        columns = colums
        )
    
    df.index = pd.to_datetime(
        df["date"] + " " + df["time"]
        )
    
    df.drop(
        columns = colums[:3], 
        inplace = True
        )
    
    df = df.replace("---", np.nan)
    
    for col in df.columns:
        df[col] = pd.to_numeric(df[col])
    
    return df

def velocity(df, col = 'hF2'):
    
    df['time'] = b.time2float(df.index.time)
    
    df['vz'] = (df[col].diff() / 
                df['time'].diff()) / 3.6
    
    df['vz'] = b.smooth2(df['vz'], 5)
    
    return df

import matplotlib.pyplot as plt
import os

def run_year():

    infile = "database/jic/sao/"
    out = []
    for file in os.listdir(infile):
        out.append(chars(infile + file))

    df = pd.concat(out).sort_index()
    save_in = 'digisonde/data/chars.txt'
    
    df.to_csv(save_in)
   # df = df.loc[df.index.time == dt.time(0, 0)]
   # df['hF2'].plot()
        
# run_year()