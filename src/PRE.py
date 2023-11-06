import pandas as pd
import numpy as np
import datetime as dt
from tqdm import tqdm 
from GEO import dusk_from_site
import base as b

pd.set_option('mode.chained_assignment', None)

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

    
