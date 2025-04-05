import pandas as pd
import base as b 
import digisonde as dg 
import datetime as dt 

 #'CAJ2M', 

def load_drift(
        site, 
        dn, 
        smooth = 3,
        cols = list(range(3, 10, 1))
        
        ):
    file = dg.dn2fn(dn, site)
    
    df = dg.IonoChar(file, cols, sum_from = None)
    
    df = df.drift(smooth)['vz'].to_frame(site)
    
    df = df.interpolate()
    
    df[site] = b.smooth2(df[site], smooth)
    
    return df

def concat_disturbed_quiet(site, dn):
    
    df = dg.quiet_time_avg(site)
    
    df = dg.renew_index_from_date(df, dn)
    
    ds = load_drift(site, dn)
    
    return pd.concat([df, ds], axis = 1)


def get_infos(ds, dn, site):
    
    delta = dt.timedelta(hours = 12)
    
    conds = [(ds.index > dn), 
             (ds.index < dn - delta)]
    
    names = ['dusk', 'sunsire']
    
    out = []
    for i, cond in enumerate(conds):
        
        df = ds.loc[cond].max().to_frame(names[i]).round(2).T
        
        df.rename(columns = {site: 'distur'}, inplace = True)
        
        df.columns = pd.MultiIndex.from_product(
            [[names[i]], df.columns]
            )
        df.index = [site]
        out.append(df)
        
    return pd.concat(out, axis = 1)


def infos_in_sites(dn, name, sites):
    out = []
    for site in sites:
    
        ds = concat_disturbed_quiet(site, dn)
    
        df = get_infos(ds, dn, site)
        
        
        out.append(df)
        
        
    return pd.concat(out)


def run_phases(dn):
    names = ["main", 'recovery']
    
    out = []
    for i, name in enumerate(names):
        delta = dt.timedelta(days = i)
        out.append(infos_in_sites(dn + delta, name))
        
        
    return pd.concat(out, axis = 1)
    
dn = dt.datetime(2015, 12, 20)

# run_phases(dn)

# name = 'main'
# infos_in_sites(dn, name)

sites = ['SAA0K', 'BVJ03']

site = sites[0]

ds = concat_disturbed_quiet(site, dn)

# ds.plot(figsize = (12, 9)) 

import GEO as gg 

site_like = site[:3].lower()

dusk = gg.dusk_from_site(
        dn, 
        site_like,
        twilight_angle = 0
        )


delta = dt.timedelta(hours = 2)

conds = []


sel_index = ds.loc[
    ((ds.index > dusk - delta) & 
    (ds.index < dusk + delta))
    ]



