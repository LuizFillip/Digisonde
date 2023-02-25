from build import paths as p
import pandas as pd
import numpy as np
from Digisonde.utils import smooth, time2float

#pd.options.mode.chained_assignment = None

def load_drift(n = None, 
               site = "SSA", 
               ext = "RAW", 
               smoothed = True, 
               resample = True):
    
    infile = p("Drift").get_files_in_dir(site)
    infile = [f for f in infile if ext in f][0]
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    if smoothed:
        df["vx"] = smooth(df["vx"], 3)
        df["vy"] = smooth(df["vy"], 3)
        df["vz"] = smooth(df["vz"], 3)
        
    if resample:
        df = df.resample("5min").last().interpolate()
        
    if n is None:
        return df
    else:
        return df.loc[df.index.month == n]

def filter_values(avg, std, df, std_factor = 1):
    
    out = []
    
    avg = avg.values
    std = std.values
    
    for col in df.columns:
        
        arr = df[col].values
        right = avg + (std_factor * std)
        left = avg - (std_factor * std)
    
        res = np.where((arr < right) & 
                       (arr > left), 
                       arr, np.nan)
        
        out.append(pd.DataFrame({col: res}, 
                                index = df.index))
        
    return pd.concat(out, axis = 1)


def pivot_data(n, col = "vx"):

    df = load_drift(n, smoothed = False)
    
    df["time"] = time2float(df.index.time)
        
    return pd.pivot_table(
        df, 
        values = col, 
        columns = df.index.date, 
        index = "time"
        )


def get_avg_std(df):
    return df.mean(axis = 1), df.std(axis = 1)

df = load_drift(1, ext = "PRO")


print(df)
