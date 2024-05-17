import pandas as pd
from base import load
import datetime as dt

def new_dataset(
        day,
        pre_value,
        periods = 67, 
        freq = '10min'
        ):
    
    dn = day + dt.timedelta(hours = 20)
    
    idx = pd.date_range(
        dn, 
        periods = periods, 
        freq = freq
        )
    
    dat = {'vzp': [pre_value] * periods}
    
    return pd.DataFrame(dat, index = idx)

def repeat_values(file):
    
    ds = load(file)
    
    ds.index = ds.index.date
    
    out = []
    
    for i, day in enumerate(ds.index):
        
        pre_value = ds.iloc[i, 0].item()
        out.append(new_dataset(
            pd.to_datetime(day), 
            pre_value)
            )
    
    return pd.concat(out)

def process_years(infile):
    
    for year in range(2016, 2023):
        
        yr = f'{year}.txt'
        df = repeat_values(infile + yr)

        df.to_csv(infile +  f'R{year}.txt')
    

year = 2023
infile = 'digisonde/data/drift/PRE/saa/'
# repeat_single_file(site = 'saa')

# yr = f'{year}.txt'
# df = repeat_values(infile + yr)

# df.to_csv(infile +  f'R{year}.txt')


df = load(infile +  f'R{year}.txt')

df.plot()