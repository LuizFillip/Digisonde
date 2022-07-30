
from ionosonde import *
import datetime
from sites import *
    


def PRE(infile, filename, 
        day = 2, delta = 1):    
    
   
    df = drift(select_day(infile, 
                          filename, 
                          day))
    time = df.index[0]
    year, month, day = time.year, time.month, time.day
       
    dusk = terminators(filename, 
                       date = datetime.date(year, month, day)).dusk
        
    df = df.loc[((df.time > (dusk - delta)) & 
                 (df.time < (dusk + delta))), :]
    
    result = {}
    
    pre = df.max().values
    times = df.idxmax().values
    
    for num, col in enumerate(df.columns[1:]):
        
        num = num + 1
        
        intime = pd.to_datetime(times[num])
           
        result[col] = list((time_to_float(intime), 
                            round(pre[num], 3)))
       
    day = pd.to_datetime(times[0]).strftime('%Y-%m-%d')
    
    tuples = list(zip([day, day], ["time", 
                                   "peak"]))
    
    index = pd.MultiIndex.from_tuples(tuples, 
                                      names=["Date", 
                                             "Values"])
    
    df = pd.DataFrame(result, index = index)  
    df.columns.name = site(filename).name
    
    return df

def main():   
    infile = "Database/FZ_2014-2015_Processado/"
    
    _, _, files = next(os.walk(infile))
    
    filename = files[9]
    
    pre = PRE(infile, filename, 
              day = 2, delta = 1)
    
    
    print(pre)

    
main()