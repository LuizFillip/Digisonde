import digisonde as dg
import numpy as np
import pandas as pd
import base as b
import GEO as gg

pd.set_option('mode.chained_assignment', None)


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

    ds["vz"] = np.mean(
        ds[columns[1:]], 
        axis = 1
        )
    
    return ds


def get_maximum_row(
        ts,
        dn, 
        site = 'saa',
        N = 5
        ):
    
    ts = ts[['vz', 'evz']]
    
    ts['max'] = ts['vz'].max()
    ts['filt'] = b.running(ts['vz'], N)
    
    ds = dg.sel_between_terminators(ts, dn, site)
    
    if len(ds) == 0:
        ds = ts.copy()
        
    ds = ds.sort_values(
        'vz',  
        ascending = False
        ).round(3)
    
    ds = ds.iloc[0, :].to_frame().T 
    ds.index = [dn]
    return ds

import datetime as dt 

def empty(dn):
    data = {'vz': np.nan, 'evz': np.nan, 
          'max': np.nan,  'filt': np.nan}
    return pd.DataFrame(data, index = [dn])

def PRE_from_SAO(infile, site):
    

    vz = vertical_drift(
         dg.fixed_frequencies(infile)
         )

    vz['evz'] = vz.std(axis = 1)
    
    out = []
    dates = np.unique(vz.index.date)
    
    for dn in pd.to_datetime(dates):
        
        delta = dt.timedelta(hours = 21)
        
        ts =  b.sel_times(
            vz, dn + delta, hours = 6
            )
        
        try:
            out.append(
                get_maximum_row(
                    ts, dn, site = site
                    )
                )
        except:
            out.append(empty(dn))
            continue
    
    return pd.concat(out)


# vz = vertical_drift(
#      dg.fixed_frequencies(infile)
#      )

# vz['evz'] = vz.std(axis = 1)

# vz

# dates = np.unique(vz.index.date)

# # for dn in pd.to_datetime(dates):
    
# dn = pd.to_datetime(dates)[0]
# delta = dt.timedelta(hours = 21)

# ts =  b.sel_times(
#     vz, dn + delta, hours = 6
#     )

# get_maximum_row(
#     ts, dn, site = 'jic'
#     )

