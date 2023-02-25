from build import paths as p
import pandas as pd
import numpy as np
from Digisonde.utils import smooth, time2float


def load_drift(n = None, 
               site = "SSA", 
               ext = "PRO", 
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
    
    
def get_avg_std(df, only_values = True):
    
    avg = df.mean(axis = 1)
    std = df.std(axis = 1)
    
    if only_values:
        return (avg.values, std.values)
    else:
        return avg, std

def filter_values(df, 
                  std_factor = 1, 
                  replace_nan = True):
    
    avg, std = get_avg_std(df)
    
    out = []
       
    for col in df.columns:
        
        arr = df[col].values
        right = avg + (std_factor * std)
        left = avg - (std_factor * std)
    
        res = np.where((arr < right) & 
                       (arr > left), 
                       arr, 
                       np.nan)
        
        
        out.append(pd.DataFrame({col: res}, 
                                index = df.index))
        
    df = pd.concat(out, axis = 1)    
    if replace_nan:
        
        df["avg"] = avg
        for col in df.columns:
            df.loc[df[col].isnull(), col] = df['avg']
            
        del df["avg"]
        return df
    else:
        return df


def pivot_data(n, col, 
               smoothed = True, 
               resample = False):

    df = load_drift(n, 
                    smoothed = smoothed, 
                    resample = resample)
    
    df["time"] = time2float(df.index.time)
        
    return pd.pivot_table(
        df, 
        values = col, 
        columns = df.index.date, 
        index = "time"
        )




df = pivot_data(1, smoothed = True, col = "vy")

avg, std = get_avg_std(df, only_values = False)
df_filtered = filter_values(df, std_factor = 1)

col = df.columns[1]

df[col].plot()
df_filtered[col].plot()