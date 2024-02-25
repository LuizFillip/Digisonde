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
    
    return ds



def time_between_terminator(df, dn, site = 'jic'):
    
    dusk = gg.dusk_from_site(
            dn, 
            site = site,
            twilight_angle = 18
            )
    
    delta = dt.timedelta(minutes = 30)
    
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
        
        
    return{'time': time, 'vp': vp, 'dusk': dusk, 'dn': dn.date()}


def running_pre(df, year):
    
    df = df.drop(columns = ['8', '9'])
    
    values = []

    for day in tqdm(range(365), str(year)):
     
         delta = dt.timedelta(days = day)
         
         dn = dt.datetime(year, 1, 1, 20) + delta
         
         try:
             ds = b.sel_times(df, dn, hours = 7).interpolate()
           
             vz = dg.vertical_drift(ds)
             values.append(time_between_terminator(vz, dn))
        
         except:
             continue
    
    return pd.DataFrame(values).set_index('dn')
    

def run_years():
    
    infile = 'digisonde/data/jic_freqs.txt'
    df = b.load(infile)
    out = []
    for year in range(2013, 2022):
        out.append(running_pre(df, year))
        
    df = pd.concat(out)
    
    df.to_csv('jic_freqs2')
    
# run_years()
# infile = 'digisonde/data/jic_freqs.txt'
# df = b.load(infile)
# year = 2015
# running_pre(df, year)