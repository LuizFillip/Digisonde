import digisonde as dg
import numpy as np
import pandas as pd
from base import (load,
    smooth2, dn2float)

def get_drift(df, col = 'hf'):
    
    df[col] = df[col].interpolate()
    
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
