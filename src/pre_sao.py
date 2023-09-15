import digisonde as dg
import numpy as np
import pandas as pd
import base as b

def get_drift(
        df, 
        set_cols = 'hf', 
        smooth = False
        ):
    
    df[set_cols] = df[set_cols].interpolate()
    
    df['vz'] = (df[set_cols].diff() / 
               df["time"].diff()) / 3.6
    
    if smooth:
        df['vz'] = b.smooth2(df['vz'], 5)
    
    return df

def vertical_drift(
        df: pd.DataFrame, 
        set_cols = None, 
        smooth = True
        ) -> pd.DataFrame:
    
    """
    Compute the vertical drift with 
    (dh`F/dt) from ionosonde fixed frequency 
    (in meters per second)
    """
    
    ds = df.copy()
    
    if set_cols is None:
        columns = ds.columns
    else:
        columns = set_cols
        
    for col in columns:
        
        if col != "time":
            
            if smooth:
                ds[col] = b.smooth2(ds[col], 5)
        
            ds[col] = (ds[col].diff() / 
                         ds["time"].diff()) / 3.6

    ds["avg"] = np.mean(
        ds[columns[1:]], axis = 1)
    
    
    return ds

def add_vzp(
        infile = "database/Digisonde/SAA0K_20130216_freq.txt"
        ):

    df = b.load(infile)
    vz = dg.drift(
        df, 
        sel_columns = [6, 7, 8, 9]
        )
    
    out = {"idx": [], "vzp": []}
    for dn in np.unique(vz.index.date):
        idx, vzp = dg.get_pre(dn, vz)
        out["idx"].append(idx.date())
        out["vzp"].append(vzp)
        
    return pd.DataFrame(out).set_index("idx")

infile = 'database/iono/SAA0K_20130101(001).TXT'
df = dg.fixed_frequencies(infile) 

vz = vertical_drift(
     df, 
     set_cols = [6, 7, 8, 9]
     )



vz