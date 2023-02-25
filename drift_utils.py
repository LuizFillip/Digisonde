from build import paths as p
import pandas as pd
import numpy as np
import os
from Digisonde.drift import load_export
from Digisonde.utils import smooth
pd.options.mode.chained_assignment = None

def load_drift(n, 
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


def get_month_avg(df, col = "vz", 
                  sample = "5min"):

    df = df.resample(sample).last().dropna()
    
    df["time"] = (df.index.hour + 
                  df.index.minute / 60)

    days = np.unique(df.index.day)
    
    out = []
    
    for day in days:
        df1 = df.loc[df.index.day == day, :]
        
        df1.rename(columns = {col: day}, 
                   inplace = True)
        df1.index = df1["time"]
        out.append(df1[day])
    
    return pd.concat(out, axis = 1)
    


def concat_files(site = "SSA_PRO", 
                 save = True):

    f = p("Drift")
    
    files = f.get_files_in_dir(site)
    out = []
    for filename in files:
        out.append(load_export(filename))
    
    df = pd.concat(out).sort_index()
    
    if save:
    
        to_save = os.path.join(f.root,
                               site[:3], 
                               "PRO_2013.txt")

        df.to_csv(to_save, index = True)
        
    return df

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
