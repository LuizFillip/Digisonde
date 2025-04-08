import pandas as pd 
import digisonde as dg 
import datetime as dt 
import base as b 
import GEO as gg 



sites = [ 'SAA0K', 'BVJ03', 'FZA0M', 'CAJ2M', 'CGK21']


def run_in_dates(site):

    out = []
    
    dates = pd.date_range(
        '2015-12-19', 
        freq = '1D', 
        periods = 4
        )
    
    for dn in dates:
        
        file =  dg.dn2fn(dn, site)
    
        ds = dg.IonoChar(
            file,  
            sum_from = None
            ).chars
        
        dusk = gg.dusk_from_site(
                dn, 
                site[:3].lower(),
                twilight_angle = 18
                )
        
        delta = dt.timedelta(hours = 2)
        
        sel_index = ds.loc[
            ((ds.index > dusk - delta) & 
            (ds.index < dusk + delta))
            ].copy()
        
        dummy = pd.DataFrame()
        dummy[dn] = [sel_index['hmF2'].max()]
        dummy.index = [site]
        
        out.append(dummy.T)
        
    return pd.concat(out).sort_index()

out = []
# for site in sites:
#     out.append(run_in_dates(site))
    
# df = pd.concat(out, axis = 1)

# df 
for site in sites:
    dn = dt.datetime(2015, 12, 21, 6)
    file =  dg.dn2fn(dn, site)
    
    ds = dg.IonoChar(
        file,  
        sum_from = None
        ).chars
    
    # ds['hmF2'].plot(figsize = (12, 6))
    delta = dt.timedelta(hours = 2)
    
    sel = ds.loc[
        ((ds.index > dn - delta) & 
        (ds.index < dn + delta))
        ].copy()
    
    data = {site: sel['hmF2'].max()}
    # print()
    out.append(pd.DataFrame(
        data, index = [sel['hmF2'].idxmax()]))
    
pd.concat(out)

