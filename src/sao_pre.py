import digisonde as dg
import numpy as np
import pandas as pd
import base as b
import datetime as dt 
import GEO as gg
import os
from tqdm import tqdm 
pd.set_option('mode.chained_assignment', None)


PATH_FREQ = 'database/jic/freq/'


def velocity(ds, col, smooth = True):
    
    if smooth:
        ds[col] = b.smooth2(ds[col], 5)

    ds[col] = (ds[col].diff() / ds["time"].diff()) / 3.6
    
    return ds.interpolate()
    

def vertical_drift(
        df: pd.DataFrame, 
        set_cols = None,
        smooth = 5
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

            ds[col] = (ds[col].diff() / ds["time"].diff()) / 3.6
    
    ds["vz"] = np.mean(ds[columns[1:]], axis = 1)
    
    
    if smooth is not None:
        for col in ds.columns:
            ds[col] = b.smooth2(ds[col], smooth)
    
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




def time_between_terminator(df, dn, site = 'jic'):
    
    dusk = gg.dusk_from_site(
            dn, 
            site = site,
            twilight_angle = 18
            )
    
    delta = dt.timedelta(hours = 1)
    
    sel = df.loc[
        (df.index > dusk - delta) &
        (df.index < dusk + delta), ['vz']
        ]
    
    if len(sel) == 0:
        return np.nan 
    else:
        return sel['vz'].idxmax(), sel.max().item()

index = []
values = []

year = 2015

infile =  f'database/jic/freq/{year}'
df = dg.freq_fixed(infile)


for day in tqdm(range(365), str(year)):
 
     delta = dt.timedelta(days = day)
     
     dn = dt.datetime(year, 1, 1, 20) + delta
     
     try:
         ds = b.sel_times(df, dn, hours = 7).interpolate()
        
         vz = dg.vertical_drift(ds)
            
         idx, vmax = time_between_terminator(vz, dn)
         
         index.append(idx)
         values.append(vmax)
     except:
         continue

df = pd.DataFrame({'vp': values}, index = index)

infile = 'jic20151'

df.to_csv(infile)