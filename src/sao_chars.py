import numpy as np
import pandas as pd
import base as b 
import os 

def velocity(df, col = 'hF2'):
    
    df['time'] = b.time2float(df.index.time)
    
    df['vz'] = (df[col].diff() / df['time'].diff()) / 3.6
    
    df['vz'] = b.smooth2(df['vz'], 5)
    
    return df

columns_e = ["date", "doy", "time", 
           'foF2', 'hF2', 'QF', 'hmF2',
           'f(h`F)', '(h`F2)']

columns_e = [
    "date", "doy", "time", 
    'foF2' ,  'hF2',  'hF',  'QF', 
    'QE', 'foEs', 'hEs', 
    'fminEs',  'fbEs',   'hmF2'
    ]
def chars(infile):
    f = open(infile).readlines()

    raw_data = [f[i].split() for i in range(2, len(f))]

    columns = ["date", "doy", "time"]
    columns.extend(f[0].split()[3:])
    
    columns = [c.replace('`', '') for c in columns]
    
    try:
        df = pd.DataFrame(raw_data, columns = columns)
    except:
        df = pd.DataFrame(raw_data, columns = columns_e)
        
    df.index = pd.to_datetime(
        df["date"] + " " + df["time"]
        )
    
    df.drop(
        columns = columns[:3], 
        inplace = True
        )
    
    df = df.replace("---", np.nan)
    
    for col in df.columns:
        df[col] = pd.to_numeric(df[col])
    
    return df

