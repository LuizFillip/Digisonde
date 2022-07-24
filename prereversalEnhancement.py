
from ionosonde import *
import matplotlib.pyplot as plt
import datetime
#from get_time_terminator import *
#from plotVerticaldrift import *







class PRE(object):
    
    def __init__(self, data):
        self.data = data
    
    
        time = self.data.index[0]
        year, month, day = time.year, time.month, time.day
        
        #try:
           # terminator = get_time_terminator(year, month, day).terminator()
           # time_sunset = terminator.time()
        #except:
        terminator = datetime.datetime(year, 
                                       month, 
                                       day, 
                                       21, 45)

        
        delta = datetime.timedelta(hours = 1)
        
        self.data = self.data.loc[((self.data.index > terminator - delta) & 
                                   (self.data.index < terminator + delta)), :]
           
        times = self.data.idxmax().values
        pre = self.data.max().values
        freqs = self.data.columns
        
        result = {}
        
        for num in range(len(times)):
        
            timestring = pd.to_datetime(times[num]).strftime('%H:%M')
            
            result[freqs[num]] = list((timestring, round(pre[num], 3)))
        
        #result["sunset"] = terminator.time()
        
        day = pd.to_datetime(times[0]).strftime('%Y-%m-%d')
        
        tuples = list(zip([day, day], ["Time (UT)", 
                                       "Peak (m/s)"]))
        
        index = pd.MultiIndex.from_tuples(tuples, 
                                          names=["Date", 
                                                 "Values"])
        
        self.df = pd.DataFrame(result, index = index)
        
        self.df.columns.name = "Frequencies (MHz)"
        
    @property
    def table(self):
        return self.df
    @property
    def terminator(self):
        return terminator
    @property
    def pre_avg(self):
        return pre.mean()

def main():    
    infile = "Database/FZ_2014-2015_Processado/"
    
    _, _, files = next(os.walk(infile))
    
    filename = files[9]
    
    
    iono = ionosonde(infile, filename)
    
    days = list(set(iono.data.index.day))
    
    for day in days:
        
        df = vertical_drift(iono.select_day(day))
        
        try:
            pre_table = PRE(df).table
        except:
            print(day)
            pass