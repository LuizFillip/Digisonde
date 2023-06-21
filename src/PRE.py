import pandas as pd
import numpy as np
from utils import time2float
import digisonde as dg
import datetime as dt
from common import load


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
    
    b = dt.time(21, 0, 0)
    e = dt.time(23, 0, 0)
    
    df = df.loc[(df.index.time >= b) & 
                (df.index.time <= e) & 
                (df.index.date == dn), [col]
                ]
        
    return df.idxmax().item(), round(df.max().item(), 3)


def get_pre_in_year(df):
    
    year = df.index[0].yeart
        
    dates = pd.date_range(
        f"{year}-1-1", 
        f"{year + 1}-1-1", 
        freq = "1D"
        )
    
    out = {"vp": [], "time": []}
    
    for dn in dates:
        
        try:
            df1 = df.loc[df.index.date == dn.date()]
            tpre, vpre = get_pre(dn.date(), df1)
            
            out["vp"].append(vpre)
            out["time"].append(tpre)
        except:
            out["vp"].append(np.nan)
            out["time"].append(np.nan)
            continue
        
        
    ds = pd.DataFrame(out, index = dates)
    
    
    
    return ds

def filter_error_vls(ds):
    ds.loc[(ds.index.month <= 4) 
           & (ds["vp"] < 10), "vp"] = np.nan
    
    ds.loc[ (ds.index.month > 9)
           & (ds["vp"] < 10), "vp"] = np.nan
    return ds


def add_vzp(
        infile = "database/Digisonde/SAA0K_20130216_freq.txt"
        ):

    df = load(infile)
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
    infile = "database/Digisonde/SAA0K_20130316(075)_freq"
    
    df = dg.fixed_frequencies(infile)
    
    vz = dg.drift(df)
    
    out = []
    for dn in np.unique(vz.index.date):
        print(get_pre(dn, vz))

