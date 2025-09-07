import pandas as pd 
import digisonde as dg 
import datetime as dt 
import base as b 
import GEO as gg 


def concat_quiet_and_disturb(site = 'SAA0K'):
      
    dn = dt.datetime(2015, 12, 19)
    
    ds = dg.join_iono_days(
            site, 
            dn,
            parameter = 'hF',
            number = 4,
            cols = list(range(3, 8, 1))
            )
    
    ds[site] = b.running(ds[site], 3)
    
    df = dg.repeat_quiet_days(site, dn)
    ds['q_mean'] = ds.index.map(df['mean'])
    ds['q_std'] = ds.index.map(df['std'])
    return ds



def test_join_drift():
    
    site = 'SAA0K'
    
    dn = dt.datetime(2015, 12, 19)
    
    df = dg.join_iono_days(
            site, 
            dn,
            parameter = 'drift',
            cols = [5, 6]
            )
    
    print(df)



sites = [ 'SAA0K', 'BVJ03', 'FZA0M', 'CAJ2M', 'CGK21']




def concat_quiet_storm(site, p):
    
    start = dt.datetime(2015, 12, 19)
    
    qt = dg.repeat_quiet_days(
         site, 
         start, 
         parameter = p, 
         )
    
    if p == 'drift':
        wsm = 10
    else:
        wsm = 3
        
    qt = qt.apply(lambda s: b.smooth2(s, wsm))
    
        
    df = dg.join_iono_days(
            site, 
            start, 
            parameter = p,
            cols = [5, 6, 7]
            )
    
    df[p] = b.smooth2(df[p], 3)
    
    df = df.loc[~df.index.duplicated(keep = 'first')]
    
    ds = pd.concat([df[p], qt['mean']], axis = 1) 
    
    ds.rename(
        columns = {p: 'storm', 'mean': 'quiet'},
        inplace = True
        )

    return ds



def summary_from_ref_time(ref_dn, site, p = 'hmF2'):
    
    ds = concat_quiet_storm(site, p)
    
    delta = dt.timedelta(hours = 2)
    
    sel = ds.loc[
        ((ds.index > ref_dn - delta) & 
        (ds.index <ref_dn + delta))
        ].copy()
    
    date = sel['storm'].idxmax()
    
    ds = sel.loc[date].to_frame().T  
    ds['time'] = date 
    ds.index = [site]
    
    return ds 

def summary_by_sites():
    
    ref_dn = dt.datetime(2015, 12, 20, 20)
    
    
    out = []
    for site in sites:
        dusk = gg.dusk_from_site(
                ref_dn, 
                site[:3].lower(),
                twilight_angle = 18
                )
    
    
        out.append(summary_from_ref_time(dusk, site))
        
    return pd.concat(out)

df = summary_by_sites()

