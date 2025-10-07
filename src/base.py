import digisonde as dg 
import datetime as dt 
import os 
import base as b 
import numpy as np

FREQ_PATH = 'digisonde/data/SAO/freqs/'
PATH_CHAR = 'digisonde/data/SAO/chars/'

def _drift(ds, sf = None, smooth = None):
    
    cols = ds.columns
    
    ds["time"] = b.time2float(
        ds.index, 
        sum_from = sf
        )
    
    for col in cols:
        
        if col != "time":                         

            ds[col] = (ds[col].diff() / ds["time"].diff()) / 3.6
            
            if smooth is not None:
                
                ds[col] = b.smooth2(ds[col], smooth)
    
    ds["vz"] = np.mean(ds[cols], axis = 1)

    return ds.replace(0, float('nan'))


class IonoChar(object):
    
    
    def __init__(
            self, 
            file, 
            cols = list(range(5, 8, 1)), 
            sum_from = None
            ):
        
        file_temp = os.path.split(file)[-1]
        code, rest = tuple(file_temp.split('_'))
        
        self.code = code
        self.site = dg.code_name(code)
        self.rest = rest
        self.cols = cols    
        self.file = file
        self.sum_from = sum_from 
        
    
    @property 
    def date(self):
        fmt = '%Y%m%d(%j).TXT'
        try:
            return dt.datetime.strptime(self.rest, fmt)
        except:
            return  None
        
    
    @property 
    def chars(self):
        
        fn = f'{self.code}_{self.rest}'

        ds = dg.chars(PATH_CHAR + fn)
        
        return self.sel_time(ds)
    
    def sel_time(self, ds):
        
        if self.sum_from is not None:
            self.dn = self.date.replace(
                hour = self.sum_from)
            return b.sel_times(
                ds, self.dn, hours = 14)
        else:
            return ds
    
    @property 
    def heights(self):
        
        try:
            ds = dg.freq_fixed(FREQ_PATH + self.file)
        except:
            ds = dg.freq_fixed(self.file)
            
        return self.sel_time(ds)[self.cols]
    
    def drift(self, smooth = None):
        
         
        """
        Compute the vertical drift with 
        (dh`F/dt) from ionosonde fixed frequency 
        (in meters per second)
        """
        
        ds = self.heights
    
        sf = self.sum_from
    
        return self.sel_time(_drift(ds, sf = sf, smooth = smooth))


import pandas as pd 

infile = 'database/supre/suppression_contour'

df = dg.freq_fixed(infile)

dates = pd.to_datetime(df.index.date) 

ds = df.loc[df.index.date == dates[0]]

_drift(ds, sf = None, smooth = None)