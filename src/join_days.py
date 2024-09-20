import pandas as pd
import base as b 
import digisonde as dg 
import datetime as dt 

b.config_labels()




def load_drift(
        site, 
        dn, 
        smooth = 3,
        cols = list(range(3, 10, 1))
        
        ):
    file = dg.dn2fn(dn, site)
    
    df = dg.IonoChar(file, cols, sum_from = None)
    
    df = df.drift(smooth)['vz'].to_frame(site)
    df = df.interpolate()
    df[site] = b.smooth2(df[site], 3)
    return df
    


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
        
        file =  dg.dn2fn(dn + delta, site)
        
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
        
        file =  dg.dn2fn(dn, site)
        
        df = dg.IonoChar(file, cols, sum_from = None)
        
        ds = df.drift(
            smooth = smooth
            ).set_index('time')['vz'].dropna()
        
        out.append(ds.sort_index().to_frame(dn.day))
        
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

start_date = dt.datetime(2015, 12, 19)

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

# def main():

sites =['CAJ2M', 'SAA0K', 'BVJ03']



def concat_disturbed_quiet(site, dn):
    
    df = quiet_time_avg(site)
    
    df = renew_index_from_date(df, dn)
    
    ds = load_drift(site, dn)
    
    return pd.concat([df, ds], axis = 1)


def get_infos(ds, dn, site):
    
    delta = dt.timedelta(hours = 12)
    
    conds = [(ds.index > dn), 
             (ds.index < dn - delta)]
    
    names = ['Pôr do sol', 'Pré amanhecer']
    
    out = []
    for i, cond in enumerate(conds):
        df = ds.loc[cond].max().to_frame(names[i]).round(2).T
        df.rename(columns = {site: 'distur'}, inplace = True)
        
        df.columns = pd.MultiIndex.from_product(
            [[names[i]], df.columns])
        df.index = [site]
        out.append(df)
        
    return pd.concat(out, axis = 1)


def infos_in_sites(dn, name):
    out = []
    for site in sites:
    
        ds = concat_disturbed_quiet(site, dn)
    
        df = get_infos(ds, dn, site)
        
        
        out.append(df)
        
        
    return pd.concat(out)


def run_phases(dn):
    names = ["Fase principal", 'Fase de recuperação']
    
    out = []
    for i, name in enumerate(names):
        delta = dt.timedelta(days = i)
        out.append(infos_in_sites(dn + delta, name))
        
        
    df = pd.concat(out, axis =1)
    
    # print(df.to_latex(decimal = ','))
    
    df

# site = 'SAA0K'

site = 'CAJ2M'
dn = dt.datetime(2015, 12, 21, 21)

ds = concat_disturbed_quiet(site, dn)
# get_infos(ds, dn)
# name = 'Fase principal'
# df = infos_in_sites(dn, name)

# ds.plot()

get_infos(ds, dn, site)