import numpy as np
import pandas as pd
import digisonde as dg
import base as b 
import datetime as dt 


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
    
    df['vz'] = (df[col].diff() /  df['time'].diff()) / 3.6
    
    df['vz'] = b.smooth2(df['vz'], 5)
    
    return df

import matplotlib.pyplot as plt

infile = "database/jic/sao/2015"


df =  velocity(
    chars(infile), col = 'hF2'
    )

dates = pd.to_datetime(
    np.unique(df.index.date)
    )

out = []
for dn in dates:
    
    delta = dt.timedelta(hours = 20)

# ds = dg.sel_between_terminators(
#         df, 
#         dn + delta, 
#         site = 'jic'
#         )

    ds = b.sel_times(
        df,
        dn + delta, 
        hours = 5
        )
    
    out.append(ds['vz'].max())
    

plt.scatter(dates, out)
  
plt.ylim([0, 50])