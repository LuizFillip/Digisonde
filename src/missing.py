import datetime as dt
import numpy as np 
import pandas as pd
from base import load, sel_times 
import os
import digisonde as dg 



def find_missing_values(a, b):
    return list(set(a) ^ set(b))


def get_missing_dates(year):
    
    
    
    infile = 'digisonde/data/drift/data/saa/'

    df = load(os.path.join(infile, 
                           f'{year}_drift.txt'))
        
    df.replace(0.0, np.nan, inplace = True)
    
    df = df.loc[~(df['evz'] > 10)]

    df = df.between_time('18:00', '23:00').dropna()
    
    a = np.unique(df.index.date)
    
    b = pd.date_range(
        dt.date(year, 1, 1), 
        dt.date(year, 12, 31),
        freq = '1D'
        )
    
    b = [c.date() for c in b]
    
    return sorted(find_missing_values(a, b))




def test(year, dn):
    
    infile = 'digisonde/data/drift/data/saa/'
    
    df = load(infile + f'{year}_drift.txt')
        
    df.replace(0.0, np.nan, inplace = True)
    
    dn = dt.datetime(year, 8, 12, 18)
    
    ts = df.between_time('18:00', '23:00')


def missing_dates_2(year):
    
    df = load( f"D:\\drift\\{year}.txt")
    ds = dg.PRE_from_SAO(f'database/iono/{year}')
    
    df1 = dg.join_drift_sao(ds, df)
    
    new_date_range = pd.date_range(
        start = f"{year}-01-01", 
        end = f"{year}-12-31", 
        freq="D")
    
    
    df1 = df1.reindex(new_date_range)
    
    return df1[df1['vz'].isna()].index
