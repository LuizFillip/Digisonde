import digisonde as dg
import numpy as np
import pandas as pd
import base as b

def vertical_drift(
        ds: pd.DataFrame, 
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
            
            if smooth is not None:
                
                ds[col] = b.smooth2(ds[col], smooth)
    
    ds["vz"] = np.mean(ds[cols], axis = 1)

    ds = ds.replace(0, float('nan'))
    return ds


def test():
    file = 'SAA0K_20151220(354).TXT'
    # digisonde/data/chars/freqs/
    cols = list(range(5, 8, 1))
    ds = dg.IonoChar(file, cols).heights 
    
    df = vertical_drift(ds, smooth= 3)
    
    df['vz'].plot()