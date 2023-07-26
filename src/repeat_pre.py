import pandas as pd
from base import load
import datetime as dt


def join_sao_and_drift(
        year = 2014, 
        col = 'vp'
        ):
    
    drift_file = f'digisonde/data/drift/PRE/saa/{year}.txt'
    sao_file = 'digisonde/data/PRE/saa/2014_2015_2.txt'
    
    df = load(drift_file)[col]
    df1 = load(sao_file)[col]
    
    df1 = df1.loc[df1.index.year == year]
    
    ds = pd.concat([df1, df]).sort_index()
    
    return ds.groupby(ds.index).first().to_frame(col)


def repated_values(
        drf, 
        freq = '10min', 
        periods = 133, 
        timestart = 20,
        col = 'vp'
        ):
    
    out = []
    for day in drf.index:
    
        dn  = day + dt.timedelta(
            hours = timestart
            )
        
        new_index = pd.date_range(
            dn, 
            periods = periods, 
            freq = freq
            )
        
        data = drf[
            drf.index == day
                         ].values.repeat(
                             periods, axis=0)
        
        out.append(pd.DataFrame(data, 
                     columns = [col],
                     index = new_index
        )
                   )
        
    return pd.concat(out)

def process_years():
    
    for year in [2013, 2014, 2015]:
        ds = join_sao_and_drift(year)
            
        df = repated_values(ds)
        save_in = f'digisonde/data/drift/PRE/SAA/R{year}.txt'
        df.to_csv(save_in)
        
