import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 



def get_infos(df, dn):

    dusk = gg.dusk_from_site(
            dn, 
            site = site,
            twilight_angle = 18
            )
    
    delta = dt.timedelta(minutes = 120)
    
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
    return pd.DataFrame(data, index = [dn.date()])

def run_year()
    outw = []
    for year in range(2013, 2023):
        
        dates = pd.date_range(f'{year}-01-01', f'{year}-12-31')
        
        infile = f'digisonde/data/drift/data/saa/{year}_drift.txt'
        
        df = b.load(infile)
        
        out = []
        for dn in tqdm(dates, str(year)):
            out.append(get_infos(df, dn))
        
        outw.append(pd.concat(out))
    
    ds = pd.concat(outw)
    
    ds.to_csv('drift_pre_test1') 