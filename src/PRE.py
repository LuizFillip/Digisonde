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


import matplotlib.pyplot as plt 
import os 
from tqdm import tqdm 

path = 'digisonde/data/reduced_freqs/FZ_2014-2015/'

site = 'fza'

def run_by_month(infile, site):
    df =  dg.IonoChar(infile).drift()
    
    dates = pd.to_datetime(np.unique(df.index.date))
    
    out = []
       
    for dn in dates:
        
        ds = df.loc[df.index.date == dn]
    
        out.append(get_infos(ds, dn, site, dicts = False))
            
    return pd.concat(out)

def run_by_year(path, site):
    
    out = []
    
    for fn in tqdm(os.listdir(path)):
        
        infile = path + fn
        
        out.append(run_by_month(infile, site))
        
    return pd.concat(out).sort_index()
    

#%%%%
# df.to_csv('fza')