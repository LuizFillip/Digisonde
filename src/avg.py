import base as b
import pandas as pd
import digisonde as dg 
import datetime as dt



class IonoAverage(object):
    
    def __init__(
            self, 
            dn, 
            cols,
            site = 'SAA0K', 
            ref = None, 
            ):
        
        self.cols = cols
        self.dn  = dn 
        self.file = self.dn2fn(self.dn, site)
        
        self.data = dg.IonoChar(
            self.file, 
            self.cols, 
            sel_from = None
            )
        
        if ref is None:
            self.ref = dn
        else:
            self.ref = ref 
            self.ref_data = dg.IonoChar(self.dn2fn(ref, site))
    
    @staticmethod        
    def dn2fn(dn, site):
        return dn.strftime(f'{site}_%Y%m%d(%j).TXT')
    
    @property
    def drift(self):
        
        out = []
        
        for parameter in self.cols:
         
            out.append(
                self.pivot_mean(
                    self.data.drift(), parameter)
                
                )
            
        ds = pd.concat(out, axis = 1)
     
        st_c = [f'd{c}' for c in self.cols]
        data = {
            'vz': ds[self.cols].mean(axis = 1), 
            'dvz': ds[st_c].mean(axis = 1)
            }
        
        df = pd.DataFrame(data, index = ds.index)
            
        df.index = self.new_index_by_ref(self.ref, df.index)
        df['vz'] = b.smooth2(df['vz'], 2)
        return df
    
    def chars(self, parameter = 'hF2'):
        
        df = self.pivot_mean(self.data.chars, parameter)
        
        df.index = self.new_index_by_ref(self.ref, df.index)
        
        return df
    
    @staticmethod
    def new_index_by_ref(ref, float_times):
        
        ref = ref.replace(hour = 0, minute = 0)
        
        out = []
        for i in float_times:
            
            hour, minutes = tuple(str(i).split('.'))
            
            minute = round(float('0.' + minutes) * 60)
            hour = int(hour)
            if hour >= 24:
                hour -= 24
                delta = dt.timedelta(
                    hours = hour, 
                    minutes = minute, 
                    days = 1
                    )
            else: 
                delta = dt.timedelta(
                    hours = hour, 
                    minutes = minute
                    )
            
            out.append(ref + delta)
             
        return out 

    @staticmethod
    def pivot_mean(df, parameter = 'hF2'):
        df['time'] = b.time2float(df.index, sum_from = 18)
        
        df['day'] = df.index.day 
        
        ds = pd.pivot_table(
            df,
            values = parameter,
            columns = 'day',
            index = 'time'
            ) 
        
        data = {
            parameter: ds.mean(axis = 1), 
            'd' + str(parameter) : ds.std(axis = 1)
            }
       
        return pd.DataFrame(data, index = ds.index)



# def main():
# file = 'SAA0K_20151202(336).TXT'


# cols = list(range(4, 8, 1))

# dn = dt.datetime(2015, 12, 2)
# ref = dt.datetime(2015, 12, 20)

# ds = IonoAverage(dn, cols, site ='SAA0K', ref = ref)

# data =  ds.data.drift()

# ds.drift 
