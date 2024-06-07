import pandas as pd
import numpy as np
import datetime as dt
from tqdm import tqdm 
from GEO import dusk_from_site
import base as b

def sel_between_terminators(
        df, 
        dn, 
        site = 'saa'
        ):
    
    dn = pd.to_datetime(dn)
    
    start = dusk_from_site(
        dn, 
        twilight_angle = 0, 
        site = site
        )
    end = dusk_from_site(
        dn, 
        twilight_angle = 18, 
        site = site
        )
    
    if end < dn:
        end += dt.timedelta(days = 1)
    
    return b.sel_dates(
        df, 
        start = start, 
        end = end
        )


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
    





def get_pre(
        dn, 
        df, 
        col = "avg", 
        dusk = True
        ):
    
    if dusk:
        df = sel_between_terminators(df, dn)

    else:
        
        df = df.loc[
            (df.index.time >= dt.time(21, 0, 0)) & 
            (df.index.time <= dt.time(23, 0, 0)) & 
            (df.index.date == dn)
            ]
        
    return df[col].idxmax(), round(df[col].max(), 3)


def get_pre_in_year(
        infile, 
        col = 'vz', 
        dusk = True
        ):
    
    df = b.load(infile)
    
    df['vz'] = b.smooth2(df['vz'], 5)
    
      
    out = {"vp": [], "time": []}
    
    dates = np.unique(df.index.date)
    year = str(dates[0].year)
    
    
    for dn in tqdm(dates, desc = year):
         
        try:
            ds = df.loc[df.index.date == dn]
            
            tpre, vpre = get_pre(
                dn, ds, col = col, dusk = dusk
                )
            
            out["vp"].append(vpre)
            out["time"].append(b.dn2float(tpre))
        except:
            out["vp"].append(np.nan)
            out["time"].append(np.nan)
            continue
        

    return pd.DataFrame(out, index = dates)

    
