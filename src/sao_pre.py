import digisonde as dg
import numpy as np
import pandas as pd
import base as b
import datetime as dt 
import GEO as gg
from tqdm import tqdm 



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
    
    ds = ds.replace(0, float('nan'))
    return ds



def time_between_terminator(df, site = 'jic'):
    dn = df.index[0]
    dusk = gg.dusk_from_site(
            dn, 
            site = site,
            twilight_angle = 18
            )
    
    delta = dt.timedelta(minutes = 60)
    
    sel = df.loc[
        (df.index > dusk - delta) &
        (df.index < dusk + delta), ['vz']
        ]
    
    
    if len(sel) == 0:
        time = np.nan
        vp = np.nan 
        
    else:
        time = sel['vz'].idxmax()
        vp = sel.max().item()
        
        
    return {'time': time, 
            'vp': vp, 
            'dusk': dusk, 
            'dn': dn.date()}


def get_values(sel):
    dn = sel.index[0]
    time = sel['vz'].idxmax()
    vp = sel.max().item()
    return {'time': time, 'vp': vp, 'dn': dn.date()}    


def running_pre(df, site = 'saa'):
    
    year  = df.index[0].year
    df = df.drop(columns = ['8', '9'])
    values = {'vp': []}
    time = []
    for day in tqdm(range(365), str(year)):
     
         delta = dt.timedelta(days = day)
         
         dn = dt.datetime(year, 1, 1, 19) + delta
         
         try:
             
             ds = b.sel_times(df, dn, hours = 5).interpolate()
             vz = dg.vertical_drift(ds)
             
             values['vp'].append(vz['vz'].max())
             time.append(dn.date())
        
         except:
             continue
    
    return pd.DataFrame(values, index = time) #.set_index('dn')
    

