import pandas as pd
import numpy as np
import os
from utils import time2float
import digisonde as dg
import datetime as dt
    

def find_maximus(df: pd.DataFrame):
    """Get maximus for """
    result = {}

    pre = df.max().values
    times = df.idxmax().values
    
    for num, col in enumerate(df.columns[1:]):
        
        num = num + 1
        
        intime = pd.to_datetime(times[num])
           
        result[col] = list(
            (time2float(intime), 
             round(pre[num], 3))
            )
        
    return result


def drift(df: pd.DataFrame) -> pd.DataFrame:
    
    """Compute the vertical drift with 
    (dh`F/dt) in meters per second"""
    
    data = df.copy()
        
    for col in data.columns:
        
        if col != "time":
        
            data[col] = (data[col].diff() / 
                         data["time"].diff()) / 3.6
    cols = df.columns[1:]
    data["avg"] = np.mean(data[cols], axis = 1)
    return data



def general_vz(vz, uy, wd, i):
    """
    A general expression for vertical plasma drift including
    the effect from meridional wind and plasma diffusion
    """
    I = np.radians(i)
    
    vz_term = vz * np.cos(I)
    uy_term = uy * np.cos(I) * np.sin(I)
    wd_term = wd * pow(np.sin(I), 2)
    
    return vz_term + uy_term - wd_term 


def get_pre(dn, df, col = "avg"):
    
    b = dt.time(21, 0, 0)
    e = dt.time(23, 0, 0)
    
    df = df.loc[(df.index.time >= b) & 
                (df.index.time <= e) & 
                (df.index.date == dn), ["avg"]]
        
    return df.idxmax().item(), round(df.max().item(), 3)


def add_vzp(infile = "database/Digisonde/SAA0K_20130316(075)_freq"):

    vz = dg.drift(dg.fixed_frequencies(infile))
    
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
        
# main()