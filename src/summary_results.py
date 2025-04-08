import pandas as pd
import base as b 
import digisonde as dg 
import datetime as dt 
import GEO as gg 

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


def extract_maximums_vls(ds, ref_time):
     
    site = ds.columns[1]
        
    delta = dt.timedelta(hours = 2)
    
    sel_index = ds.loc[
        ((ds.index > ref_time - delta) & 
        (ds.index < ref_time + delta))
        ].copy()
    
    sel_index.rename(
        columns = {site: 'storm'}, 
        inplace = True
        )
    
    return sel_index.max().to_frame(site).T.round(2)

def run_comparation_by_sites(
         
        sites
        ):
    
    out_dusk = []
    out_dawn = []
    
    dusk_dn = dt.datetime(2015, 12, 20)
    dawn_dn = dt.datetime(2015, 12, 21)
    
    
    storm_dn = dt.datetime(2015, 12, 21, 6)
    
    for site in sites:
    
        ds = concat_disturbed_quiet(site, dusk_dn)
        
        dusk = gg.dusk_from_site(
                dusk_dn, 
                site[:3].lower(),
                twilight_angle = 18
                )
        
        out_dusk.append(extract_maximums_vls(ds, dusk))
        
        ds1 = concat_disturbed_quiet(site, dawn_dn)
        
        out_dawn.append(extract_maximums_vls(ds1, storm_dn))
        
    dusk_df = pd.concat(out_dusk)
    dawn_df = pd.concat(out_dawn)
    
    return dusk_df, dawn_df

sites = [ 'SAA0K', 'BVJ03', 'FZA0M', 'CAJ2M', 'CGK21']


run_comparation_by_sites(
         
        sites
        )

