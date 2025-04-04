import os 
import pandas as pd 
import datetime as dt 

root = 'E:/ionogram/'

start = dt.datetime(2015, 12, 20, 21)

times = pd.date_range(start, freq = '2H', periods = 8)

dn = times[0]

sites = [ 'SAA0K', 'BVJ03', 'FZA0M', 'CAJ2M', 'CGK21']


site = sites[0]

# def folder_dir(dn):

    # fmt = f'%Y/%Y%m%d{site[0]}'
    
    # dir_month = start.strftime(f'%Y/%Y%m%d{site[0]}')
    
    # files = os.listdir(f'{root}{dir_month}')
    
    
# for 
year = 2015
path_year = f'{root}{year}/'

for name in os.listdir(path_year):
    
    mr = 'C'
    if mr in name:
        
        
        new_name = name.replace(mr, 'CA')
        src = f'{path_year}{name}'
        dst = f'{path_year}{new_name}'
        os.rename(src, dst)