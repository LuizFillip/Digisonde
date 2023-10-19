import digisonde as dg
import numpy as np
import pandas as pd
import base as b
import datetime as dt 
import matplotlib.pyplot as plt 
import os
from tqdm import tqdm 
pd.set_option('mode.chained_assignment', None)


PATH_FREQ = 'database/jic/freq/'


def velocity(
        ds, col, 
        smooth = True
        ):
    if smooth:
        ds[col] = b.smooth2(ds[col], 5)

    ds[col] = (ds[col].diff() / 
               ds["time"].diff()) / 3.6
    
    return ds.interpolate()
    

def vertical_drift(
        df: pd.DataFrame, 
        set_cols = None
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
            ds[col] = b.smooth2(ds[col], 5)

            ds[col] = (ds[col].diff() / 
                   ds["time"].diff()) / 3.6
            
    ds["vz"] = np.mean(
        ds[columns[1:]], 
        axis = 1
        )
    
    midnight = (ds.index.time == dt.time(0, 0))
    ds.loc[midnight] = np.nan
    
    return ds


def get_maximum_row(
        ts,
        dn, 
        site = 'saa',
        N = 5
        ):
        
    ts['max'] = ts['vz'].max()
    ts['filt'] = b.running(ts['vz'], N)
    
    ds = dg.sel_between_terminators(
        ts, dn, site)
    
    if len(ds) == 0:
        ds = ts.copy()
        
    ds = ds.sort_values(
        'vz',  
        ascending = False
        ).round(3)
    
    ds = ds.iloc[0, :].to_frame().T 
    ds.index = [dn]
    return ds


def empty(dn):
    data = {
        'vz': np.nan, 
        'evz': np.nan, 
        'max': np.nan, 
        'filt': np.nan
        }
    return pd.DataFrame(data, index = [dn])



def check_night(ts):
    
    drop_ts = ts.dropna(subset = 'vz')

    if len(drop_ts) < 5:
        return np.nan
    else:
        return drop_ts.interpolate()


def data_pre(ts, dn):
    
    ts = check_night(ts)
    
    try:
        out = {'vz': ts['vz'].max()}
    except:
        out = {'vz': np.nan}
    
    return pd.DataFrame(
        out, index = [dn])


def unique_dates(df, hours = 21):
    
    dates = pd.to_datetime(
        np.unique(df.index.date)
        )
    delta = dt.timedelta(hours)
    
    return [d + delta for d in dates]

def run():
    
    out = []
    for fname in tqdm(os.listdir(PATH_FREQ)):
    
        infile = os.path.join(
            PATH_FREQ, 
            fname
            )
        
        vz = vertical_drift(
             dg.freq_fixed(infile)
             )
        
        for dn in unique_dates(vz):
            
            ds = b.sel_times(
                    vz, dn, hours = 8
                    )
            
            out.append(data_pre(ds, dn))
            
            
    return pd.concat(out).sort_index()




# df = run()



# infile = 'digisonde/data/PRE/jic/2013_2021_2.txt'
# df.to_csv(infile)