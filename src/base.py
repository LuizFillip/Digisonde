import digisonde as dg 
import datetime as dt 
import os 
import base as b 

FREQ_PATH = 'digisonde/data/chars/freqs/'
PATH_CHAR = 'digisonde/data/chars/midnight/'




class IonoChar(object):
    
    
    def __init__(
            self, 
            file, 
            cols = list(range(5, 8, 1)), 
            sum_from = 20
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
            self.dn = self.date.replace(hour = self.sum_from)
            return b.sel_times(ds, self.dn, hours = 14)
        else:
            return ds
    
    @property 
    def heights(self):
        
        ds = dg.freq_fixed(FREQ_PATH + self.file)
            
        # ds = ds[self.cols].interpolate()
        
        return self.sel_time(ds)[self.cols]
    
    def drift(self, smooth = 3):
        
        df = dg.vertical_drift(
            self.heights, 
            smooth, 
            sum_from = self.sum_from
            )
        
        return self.sel_time(df)


