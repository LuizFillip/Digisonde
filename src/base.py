import digisonde as dg 
import base as b 
import datetime as dt 
import os 


FREQ_PATH = 'digisonde/data/chars/freqs/'

code_name = {
    "FZA0M": "Fortaleza",
    "SAA0K": "São Luis", 
    "BLJ03": "Belem", 
    "BVJ03": "Boa Vista",
    "CGK21": "Campo Grande",
    "CAJ2M": "Cachoeira Paulista",
    "SMK29": "Santa Maria",
    }


class IonoChar(object):
    
    
    def __init__(self, file):
        
        file_temp = os.path.split(file)[-1]
        code, rest = tuple(file_temp.split('_'))
        
        self.site = code_name[code]
        self.rest = rest
            
        self.file = file
    
    @property 
    def date(self):
        fmt = '%Y%m%d(%j).TXT'
        try:
            return dt.datetime.strptime(
                self.rest, fmt
                )
        except:
            return  None
        
    def drift(self, set_cols = None, smooth = 5):
        
        ds = self.heights
    
        return dg.vertical_drift(ds, set_cols, smooth)
    
    def chars(self):
        
        return 
    
    @property 
    def heights(self):
        
        try:
            return dg.freq_fixed(FREQ_PATH + self.file)
        except:
            return dg.freq_fixed(self.file)
    


# file = 'FZA0M_20151220(354).TXT'
# file = 'digisonde/data/fixed_frequencies/FZ_2014-2015/FZA0M_201512.txt'
# IonoChar(file).heights
