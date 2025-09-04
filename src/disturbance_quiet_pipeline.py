import pandas as pd
import base as b 
import digisonde as dg 
import datetime as dt 


dates = [
    dt.datetime(2015, 12, 13, 9),
    dt.datetime(2015, 12, 16, 9), 
    dt.datetime(2015, 12, 18, 9),
    dt.datetime(2015, 12, 29, 9)
    ]



def smooth_in_time(df, dn, window = 3):
    
    delta = dt.timedelta(hours = 19)
    
    end = dn + delta
    
    df.loc[dn: end] = b.smooth2(df.loc[dn: end], 10)
    
    # .rolling(
    #     window = window, 
    #     center = True
    #     ).mean()
    
    return df


def quiettime_drift(
        site = 'SAA0K',
        cols = [5, 6], 
        window = 7
        ):
    
    out = []
    
    for dn in dates:
        
        file =  dg.dn2fn(dn, site)
        
        ds = dg.IonoChar(file, cols).drift()
        
        ds = ds.loc[ds.index.date == dn.date()]
        
        df = ds.set_index('time')
        
        out.append(df['vz'].to_frame(dn.day).dropna())
    
 
    df = pd.concat(out, axis = 1).sort_index()
    
    ds = pd.DataFrame()
    ds['vz'] = df.mean(axis = 1)
    ds['svz'] = df.std(axis = 1)
    
    if window is not None:
        ds = ds.apply(lambda s: b.smooth2(s, window))

    return ds 
    

def chars_time_avg( 
        site = 'SAA0K',  
        parameter = 'hF', 
        window = 1
        ):
       
    out = []
    
    for dn in dates:
        
        file =  dg.dn2fn(dn, site)
        
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
    
    data =  {'mean': df.mean(axis = 1),
             'std':  df.std(axis = 1)}
    return  pd.DataFrame(data, index  = df.index)

def repeat_quiet_days(
        site, 
        start_date,
        parameter = 'hF',
        number = 4,
        cols = [5, 6], 
        window = 3
        ):

    out = []
    
    for day in range(number):
        
        delta = dt.timedelta(days = day)
    
        dn = start_date + delta
        
        if parameter == 'drift':
            
            df = quiettime_drift(
                    site,
                    cols = cols, 
                    window = window
                    )
            
            df = df[~df.index.isna()]
            
        else:
            df = chars_time_avg( 
                    site,  
                    parameter, 
                    window = window
                    )
            
            df = df.iloc[2:-4] 
        
        out.append(b.renew_index_from_date(df, dn))
        
    return pd.concat(out) 




def join_iono_days(
        site, 
        dn,
        parameter = 'drift',
        periods = 4,
        window = 3,
        cols = [5, 6]
        ):
    
    """
    Join storm-time days
    """
    base_parameters = ['hF', 'hmF2', 'foF2', 'hF2']
    out = []
    dates = pd.date_range(dn, periods = periods, freq = '1D')
    for date in dates:
        
        file = dg.dn2fn(date, site)
        
        df = dg.IonoChar(file, cols)
        
        if parameter == 'drift':
            
            df = df.drift()
            
            out.append(df['vz'].to_frame(site))
            
        elif parameter in base_parameters:
            
            out.append(df.chars )

        else:
            out.append(df.heights)
        
    return pd.concat(out).sort_index()


def concat_quiet_and_disturb(site = 'SAA0K'):
      
    dn = dt.datetime(2015, 12, 19)
    
    ds = join_iono_days(
            site, 
            dn,
            parameter = 'hF',
            number = 4,
            cols = list(range(3, 8, 1))
            )
    
    ds[site] = b.running(ds[site], 3)
    
    df = repeat_quiet_days(site, dn)
    ds['q_mean'] = ds.index.map(df['mean'])
    ds['q_std'] = ds.index.map(df['std'])
    return ds



def test_join_drift():
    
    site = 'SAA0K'
    
    dn = dt.datetime(2015, 12, 19)
    
    df = join_iono_days(
            site, 
            dn,
            parameter = 'drift',
            cols = [5, 6]
            )
    
    print(df)

def test_smmoth_drift():
    

    site = 'SAA0K'
    dn = dt.datetime(2015, 12, 19)
        
    
    file = dg.dn2fn(dn, site)
    
    ds = dg.IonoChar(
        file, 
        cols = [5, 6], 
        sum_from = None
        ).drift()
    
    ds = smooth_in_time(ds, dn)

def test_():
    #'FZA0M', 'SAA0K', 'BVJ03'
    
    # site ='FZA0M'
    # ds = quiettime_drift(
    #         site ,
    #         cols = [5, 6]
    #         )
    
    df = quiettime_drift(
            site = 'SAA0K',
            cols = [5, 6], 
            window = 3
            )


# test_join_drift()