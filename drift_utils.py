from build import paths as p
import pandas as pd
import numpy as np
import os
from Digisonde.drift import load_export


def load_drift(n, site = "SSA"):
    
    infile = p("Drift").get_files_in_dir(site)
    infile = [f for f in infile if "RAW" in f][0]
    df = pd.read_csv(infile, index_col = 0)
    df.index = pd.to_datetime(df.index)
    
    return df.loc[df.index.month == n + 1]

def get_month_avg(df, col = "vz"):

    df = df.resample("5min").last().dropna()
    
    df["time"] = (df.index.hour + df.index.minute /60)

    days = np.unique(df.index.day)
    
    out = []
    
    for day in days:
        df1 = df.loc[df.index.day == day, :]
        df1.rename(columns = {col: day}, inplace = True)
        df1.index = df1["time"]
        
        out.append(df1[day])
    
    return pd.concat(out, axis = 1)
    


def concat_files(site = "SSA", 
                 save = True):

    f = p("Drift")
    
    out = []
    for filename in f.get_files_in_dir(site)[1:]:
    
        out.append(load_export(filename))
    
    df = pd.concat(out)
    
    if save:
    
        to_save = os.path.join(f.root, site, "PRO_2013.txt")

        df.to_csv(to_save, index = True)
        
    return df

