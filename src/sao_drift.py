import digisonde as dg
import numpy as np
import pandas as pd
import base as b
import datetime as dt 



PATH_FREQ = 'database/jic/freq/'


def velocity(ds, col, smooth = True):
    
    if smooth:
        ds[col] = b.smooth2(ds[col], 5)

    ds[col] = (ds[col].diff() / ds["time"].diff()) / 3.6
    
    return ds.interpolate()
    

def vertical_drift(
        ds: pd.DataFrame, 
        set_cols = None,
        smooth = None
        ) -> pd.DataFrame:
    
    """
    Compute the vertical drift with 
    (dh`F/dt) from ionosonde fixed frequency 
    (in meters per second)
    """
    
    cols = ds.columns
    
    ds["time"] = b.time2float(ds.index, sum_from = 15)
    
    for col in cols:
        
        if col != "time":                         

            ds[col] = (ds[col].diff() / ds["time"].diff()) / 3.6
    
    ds["vz"] = np.mean(ds[cols], axis = 1)
    # print(cols[:-1])
    
    if smooth is not None:
        for col in cols:
            ds[col] = b.smooth2(ds[col], smooth)
    
    ds = ds.replace(0, float('nan'))
    return ds


# def test():
file = 'SAA0K_20151202(336).TXT'
cols = list(range(5, 8, 1))
ds = dg.IonoChar(file, cols).heights 

df = vertical_drift(ds, smooth=None)

df