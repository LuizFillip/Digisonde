import pandas as pd
import numpy as np
import digisonde as dg
import datetime as dt
from common import load_by_time
from utils import smooth2

def get_drift(df, col = 'hf'):
    
    df['vz'] = (df[col].diff() / 
               df["time"].diff()) / 3.6
    
    df['vz'] = smooth2(df['vz'], 5)
    
    return df

def vertical_drift(
        df: pd.DataFrame, 
        sel_columns = None
        ) -> pd.DataFrame:
    
    """
    Compute the vertical drift with 
    (dh`F/dt) from ionosonde fixed frequency 
    (in meters per second)
    """
    
    data = df.copy()
    
    if sel_columns is not None:
        columns = data.columns
    else:
        columns = sel_columns
        
    for col in columns:
        
        if col != "time":
        
            data[col] = (data[col].diff() / 
                         data["time"].diff()) / 3.6

    data["avg"] = np.mean(data[columns[1:]], axis = 1)
    return data

def get_pre(dn, df, col = "avg"):
    
    
    df = df.loc[
        (df.index.time >= dt.time(21, 0, 0)) & 
        (df.index.time <= dt.time(23, 0, 0)) & 
        (df.index.date == dn), [col]
        ]
        
    return df.idxmax().item(), round(df.max().item(), 3)


def get_pre_in_year(df, col = 'vz'):
      
    out = {"vp": [], "time": []}
    
    dates = np.unique(df.index.date)
    
    for dn in dates:
         
        try:
            ds = df.loc[df.index.date == dn]
            tpre, vpre = get_pre(
                dn, ds, col = col
                )
            
            out["vp"].append(vpre)
            out["time"].append(tpre)
        except:
            out["vp"].append(np.nan)
            out["time"].append(np.nan)
            continue
        

    return pd.DataFrame(out, index = dates)

def filter_error_vls(ds):
    ds.loc[(ds.index.month <= 4) 
           & (ds["vp"] < 10), "vp"] = np.nan
    
    ds.loc[ (ds.index.month > 9)
           & (ds["vp"] < 10), "vp"] = np.nan
    return ds


def add_vzp(
        infile = "database/Digisonde/SAA0K_20130216_freq.txt"
        ):

    df = load_by_time(infile)
    vz = dg.drift(
        df, 
        sel_columns = [6, 7, 8]
        )
    
    out = {"idx": [], "vzp": []}
    for dn in np.unique(vz.index.date):
        idx, vzp = get_pre(dn, vz)
        out["idx"].append(idx.date())
        out["vzp"].append(vzp)
        
    return pd.DataFrame(out).set_index("idx")


def main():
    df = load_by_time('2013_drift.txt')
    
    df['vz'] = smooth2(df['vz'], 10)
    
    ds = get_pre_in_year(df)
    
    ds['vp'].plot()
    
    ds.to_csv('database/Drift/PRE/SAA/2013.txt')
    
