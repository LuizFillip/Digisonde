import pandas as pd
import base as b 
import digisonde as dg 
import datetime as dt 

b.config_labels()


    
def dn2fn(dn, site):
    return dn.strftime(f'{site}_%Y%m%d(%j).TXT')

def join_iono_days(
        site, 
        dn,
        parameter = 'drift',
        number = 4,
        smooth = 3,
        cols = list(range(3, 8, 1))
        ):

    out = []
    
    for i in range(number):
        
        delta = dt.timedelta(days = i)
        
        file =  dn2fn(dn + delta, site)
        
        df = dg.IonoChar(file, cols, sum_from = None)
        
        if parameter == 'drift':
            
            out.append(df.drift(smooth)['vz'].to_frame(site))
        else:
            out.append(df.heights)
        
    return pd.concat(out).sort_index()


    
dates = [
  #  dt.datetime(2015, 12, 2, 9), 
    dt.datetime(2015, 12, 13, 9),
    dt.datetime(2015, 12, 16, 9), 
    dt.datetime(2015, 12, 18, 9),
    dt.datetime(2015, 12, 29, 9)
    ]


def quiet_time_avg(
        site = 'SAA0K',
        cols = list(range(3, 10, 1)), 
        smooth = 3
        ):
    out = []
    
    for dn in dates:
        
        file =  dn2fn(dn, site)
        
        df = dg.IonoChar(file, cols, sum_from = None)
                
        ds = df.drift(
            smooth = smooth
            )
        
        ds = ds.loc[ds.index.date == dn.date()]
                
        sel_vz = ds.set_index('time')['vz'].dropna()
        
        out.append(sel_vz.sort_index().to_frame(dn.day))
        
    df = pd.concat(out, axis = 1).mean(axis = 1)
    
    return df.sort_index().iloc[:-1]
    

def float_to_time2(float_time):
    import math 
    
    minute, hour = math.modf(float_time)
  
    return hour, minute * 60


def renew_index_from_date(df, dn):
    dn = dn.replace(hour = 0, minute = 0)
    out = []
    for t in df.index:
        try:
            hour, minute = float_to_time2(t)
            
            delta = dt.timedelta(
                hours = hour, 
                minutes = minute
                )
            out.append(dn + delta)
        except:
            
            continue
        
    df.index = out 
    
    return df.to_frame('quiet')


def repeat_quiet_days(
        site, 
        start_date,
        number = 4
        ):

    out = []
    
    for i in range(number):
        
        delta = dt.timedelta(days = i)
    
        dn = start_date + delta
        
        df = quiet_time_avg(site)
        
        out.append(renew_index_from_date(df, dn))
        
    return pd.concat(out)


# site = 'FZA0M'
# quiet_time_avg(
#         site,
#         cols = list(range(3, 10, 1)), 
#         smooth = 3
#         )