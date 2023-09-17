import datetime as dt
import numpy as np 
import pandas as pd
from base import load 



def find_missing_values(a, b):
    return list(set(a) ^ set(b))


def get_missing_dates(year):
    
    
    
    infile = 'digisonde/data/drift/data/saa/'

    df = load(infile + f'{year}_drift.txt')
        
    df = df.loc[df.index.time > dt.time(18, 0)]
    
    a = np.unique(df.index.date)
    
    b = pd.date_range(
        dt.date(year, 1, 1), 
        dt.date(year, 12, 31),
        freq = '1D')
    
    b = [c.date() for c in b]
    
    return sorted(find_missing_values(a, b))

year = 2014  
get_missing_dates(year)