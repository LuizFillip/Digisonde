import numpy as np
import pandas as pd
import base as b 
import os



def chars(infile):
    f = open(infile).readlines()
    
    raw_data = [f[i].split() for i 
                in range(2, len(f))]
    
    try:    
        colums = [
            "date", "doy", "time", 
            'foF2', 'hF2', 'QF', 
            'hmF2', 'f(hF)', 'f(hF2)'
            ]
        
        df = pd.DataFrame(
            raw_data, 
            columns = colums
            )
    except:
        colums = [
            "date", "doy", "time", 
            'foF2', 'hF2', 'hF', 'QF', 
            'hmF2'
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
    
    df['vz'] = (df[col].diff() / df['time'].diff()) / 3.6
    
    df['vz'] = b.smooth2(df['vz'], 5)
    
    return df


def run_year(site = 'jic'):

    infile = f"database/{site}/sao/"
    out = []
    for file in os.listdir(infile):
        out.append(chars(infile + file))

    df = pd.concat(out).sort_index()
    save_in = f'digisonde/data/{site}_chars.txt'
    
    df.to_csv(save_in)
   

    out = [] 
    infile = 'digisonde/data/chars/'
    
    for file in ['SAA0K_20230101(001).TXT', 
                 'SAA0K_20230702(183).TXT']:
        
        out.append(chars(infile + file))
        
    df = pd.concat(out)
    
    df.to_csv('digisonde/data/chars/chars/saa_2023')