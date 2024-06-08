import digisonde as dg 
import datetime as dt 
import os 
import base as b 

FREQ_PATH = 'digisonde/data/chars/freqs/'
PATH_CHAR = 'digisonde/data/chars/midnight/'

code_name = {
    'JI91J': 'Jicamarca',
    "FZA0M": "Fortaleza",
    "SAA0K": "São Luis", 
    "BLJ03": "Belem", 
    "BVJ03": "Boa Vista",
    "CGK21": "Campo Grande",
    "CAJ2M": "Cachoeira Paulista",
    "SMK29": "Santa Maria",
    }


class IonoChar(object):
    
    
    def __init__(
            self, 
            file, 
            cols = list(range(5, 8, 1)), 
            sel_from = 20
            ):
        
        file_temp = os.path.split(file)[-1]
        code, rest = tuple(file_temp.split('_'))
        
        self.code = code
        self.site = code_name[code]
        self.rest = rest
        self.cols = cols    
        self.file = file
        self.sel_from = sel_from 
        
    
    @property 
    def date(self):
        fmt = '%Y%m%d(%j).TXT'
        try:
            return dt.datetime.strptime(self.rest, fmt)
        except:
            return  None
        
    def drift(self, smooth = 3):
        df = dg.vertical_drift(self.heights, smooth)
        return self.sel_time(df)
    
    @property 
    def chars(self):
        
        fn = f'{self.code}_{self.rest}'

        ds = dg.chars(PATH_CHAR + fn)
        
        return self.sel_time(ds)
    
    def sel_time(self, ds):
        
        if self.sel_from is not None:
            self.dn = self.date.replace(hour = self.sel_from)
            return b.sel_times(ds, self.dn, hours = 14)
        else:
            return ds
    
    @property 
    def heights(self):
        
        ds = dg.freq_fixed(FREQ_PATH + self.file)
            
        ds = ds[self.cols].interpolate()
        
        return self.sel_time(ds)
    

