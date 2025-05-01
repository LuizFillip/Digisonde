import pandas as pd
import base as b 
import digisonde as dg 
import datetime as dt 

b.config_labels()


    
def dn2fn(dn, site):
    return dn.strftime(f'{site}_%Y%m%d(%j).TXT')


    
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
    

def get_time_avg_chars( 
        site = 'SAA0K',  
        parameter = 'hF'
        ):
       
    out = []
    
    for dn in dates:
        
        file =  dn2fn(dn, site)
        
        ds = dg.IonoChar(
            file, 
            cols = None, 
            sum_from = None
            ).chars
            
        ds = ds.loc[ds.index.date == dn.date()]
        
        ds["time"] = b.time2float(
            ds.index, sum_from = None)
        
        ds = ds.set_index('time')
        
        out.append(ds[parameter].to_frame(dn.day))
        
    df = pd.concat(out, axis = 1)
    mean = b.running(df.mean(axis = 1), 3)
    std =  b.running(df.std(axis = 1), 3)
    
   
    return  pd.DataFrame({'mean':  mean, 
                          'std':  std}, index  = df.index)

def repeat_quiet_days(
        site, 
        start_date,
        parameter = 'hF',
        number = 4
        ):

    out = []
    
    for i in range(number):
        
        delta = dt.timedelta(days = i)
    
        dn = start_date + delta
        
        df = get_time_avg_chars(site, parameter)
        
        out.append(b.renew_index_from_date(df, dn))
        
    return pd.concat(out) 

def join_iono_days(
        site, 
        dn,
        parameter = 'drift',
        number = 4,
        smooth = 3,
        cols = list(range(3, 8, 1))
        ):
    
    base_parameters = ['hF', 'hmF2', 'foF2', 'hF2']
    out = []
    
    for i in range(number):
        
        delta = dt.timedelta(days = i)
        
        file =  dn2fn(dn + delta, site)
        
        df = dg.IonoChar(file, cols, sum_from = None)
        
        if parameter == 'drift':
            
            out.append(df.drift(smooth)['vz'].to_frame(site))
            
        elif parameter in base_parameters:
            
            df = df.chars 
            # df[parameter] = b.smooth2(df[parameter], smooth)
            out.append(df[parameter].to_frame(site))
            
        else:
            out.append(df.heights)
        
    return pd.concat(out).sort_index()


def concat_quiet_and_disturb():
    

    # df = get_time_avg_chars()
    
    site = 'SAA0K'
    
    dn = dt.datetime(2015, 12, 19)
    
    ds = join_iono_days(
            site, 
            dn,
            parameter = 'hF',
            number = 4,
            smooth = 3,
            cols = list(range(3, 8, 1))
            )
    
    ds[site] = b.running(ds[site], 3)
    
    df = repeat_quiet_days(site, dn)
    ds['q_mean'] = ds.index.map(df['mean'])
    ds['q_std'] = ds.index.map(df['std'])
    return ds




# concat_quiet_and_disturb()