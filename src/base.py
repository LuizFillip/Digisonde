import digisonde as dg 
import datetime as dt 
import os 


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
    
    
    def __init__(self, file, cols = list(range(5, 8, 1))):
        
        file_temp = os.path.split(file)[-1]
        code, rest = tuple(file_temp.split('_'))
        
        self.code = code
        self.site = code_name[code]
        self.rest = rest
        self.cols = cols    
        self.file = file
    
    @property 
    def date(self):
        fmt = '%Y%m%d(%j).TXT'
        try:
            return dt.datetime.strptime(self.rest, fmt)
        except:
            return  None
        
    def drift(self, set_cols = None, smooth = None):
        

        return dg.vertical_drift(self.heights, set_cols, smooth)
    
    @property 
    def chars(self):
        
        fn = f'{self.code}_{self.rest}'

        return dg.chars(PATH_CHAR + fn)
    
    @property 
    def heights(self):
        
        try:
            ds = dg.freq_fixed(FREQ_PATH + self.file)
        except:
            ds  = dg.freq_fixed(self.file)
            
        return ds[self.cols].interpolate()
    

