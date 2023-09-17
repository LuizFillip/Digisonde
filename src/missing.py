import datetime as dt
import numpy as np 
import pandas as pd
from base import load, sel_times 
import os


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


# miss_data