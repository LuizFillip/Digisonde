import os 
import pandas as pd 
import datetime as dt 
import base as b 

start = dt.datetime(2015, 12, 20, 21)

times = pd.date_range(start, freq = '2H', periods = 8)

dn = times[0]

sites = [ 'SAA0K', 'BVJ03', 'FZA0M', 'CAJ2M', 'CGK21']


site = sites[0]

# def folder_dir(dn):

    # fmt = f'%Y/%Y%m%d{site[0]}'
    
    # dir_month =
    
    # files = os.listdir(f'{root}{dir_month}')


def closest_iono(target, path_in):
    iono_times = [
        fn2dn(f) for f in
        os.listdir(path_in) if 'PNG' in f ]
  
    return b.closest_datetime(iono_times, target)


def dn2fn(dn, site):
    return dn.strftime(f'{site}_%Y%m%d(%j).TXT')

def fn2dn(filename):
    
    args = filename.split("_")
    
    try:
        date_str = args[1][:8] + args[1][13:-4]
        fmt =  "%Y%m%d%H%M%S"
        return dt.datetime.strptime(date_str, fmt)
    
    except:
        date_str = args[1].split('.')[0]
        fmt = "%Y%m%d(%j)%H%M%S"
        return dt.datetime.strptime(date_str, fmt)

        

class IonoDir(object):
    
    def __init__(self, site, dn):
        
        self.site = site
        self.dn = dn 
        self.root = 'E:/ionogram/'

    @property
    def name_folder(self):
        fmt = f'%Y/%Y%m%d{self.site[:2]}'
        return self.dn.strftime(fmt)
    
    @property
    def folder_path(self):
        return f'{self.root}{self.name_folder}'
    
    @property
    def dn2PNG(self):
        fmt = f'{self.site}_%Y%m%d(%j)%H%M%S.PNG'
        return self.dn.strftime(fmt)
    
    @property 
    def list_full_paths(self):
        
        files = os.listdir(self.folder_path)
        
        return [f'{self.folder_path}/{f}' for f in files]
    
    def get_time_list(self, ext = 'PNG'):
        
        files = os.listdir(self.folder_path)
        
        return [fn2dn(f) for f in files if ext in f]
    
    @property 
    def path_from_dn(self):
        
        return f'{self.folder_path}/{self.dn2PNG}'
        
    
  

p = IonoDir(site, dn)

p.path_from_dn
