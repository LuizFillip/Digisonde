import pandas as pd
import numpy as np
import datetime as dt
import digisonde as dg 
import GEO as gg 



def get_infos(df, dn, site = 'jic', dicts = True):

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
    
    data = {'time': time, 'vp': vp, 'dusk': dusk}
    if dicts:
        return data
    else:
        return pd.DataFrame(data, index = [dn.date()])


def pre_getting(file, site = 'bvj'):
    
    cols = list(range(5, 9, 1))
    ds = dg.IonoChar(file, cols, sel_from = None).heights 
    df = dg.vertical_drift(ds, smooth= 3)
        
    dates = sorted(list(set(df.index.date)))
    
    out = []
   
    for date in dates:
        
        dn = dt.datetime.combine(date, dt.time(21,0))
        
        out.append(get_infos(df, dn, site))
        
    return pd.concat(out)


def run_by_files(files):
    
    return pd.concat([pre_getting(f) for f in files])




file = 'BVJ03_20130812(224).TXT'


files = [
    # 'BVJ03_20130812(224).TXT',
    'BVJ03_20140101(001).TXT', 
    'BVJ03_20140701(182).TXT', 
    'BVJ03_20150701(182).TXT',
    'BVJ03_20150701(182).TXT',
    'BVJ03_20160101(001).TXT',
    'BVJ03_20170328(087).TXT',
    # 'BVJ03_20170921(264).TXT'
    ]



# df = run_by_files(files)


# df.to_csv('digisonde/data/PRE/bvj/2013_2021.txt')