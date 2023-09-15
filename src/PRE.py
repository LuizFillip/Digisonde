import pandas as pd
import numpy as np
import datetime as dt
from tqdm import tqdm 
from GEO import sun_terminator
import base as b
import digisonde as dg

def sel_between_terminators(df, dn):
    
    dn = pd.to_datetime(dn)
    start = sun_terminator(dn, twilight_angle = 0)
    end = sun_terminator(dn, twilight_angle = 18)
    
    return b.sel_dates(df, start = start, end = end)



def get_pre(dn, df, col = "avg", dusk = True):
    
    if dusk:
        df = sel_between_terminators(df, dn)

    else:
        
        df = df.loc[
            (df.index.time >= dt.time(21, 0, 0)) & 
            (df.index.time <= dt.time(23, 0, 0)) & 
            (df.index.date == dn)
            ]
        
    return df[col].idxmax(), round(df[col].max(), 3)


def get_pre_in_year(
        infile, 
        col = 'vz', 
        dusk = True
        ):
    
    df = b.load(infile)
    
    df['vz'] = b.smooth2(df['vz'], 5)
    
      
    out = {"vp": [], "time": []}
    
    dates = np.unique(df.index.date)
    year = str(dates[0].year)
    
    
    for dn in tqdm(dates, desc = year):
         
        try:
            ds = df.loc[df.index.date == dn]
            
            tpre, vpre = get_pre(
                dn, ds, col = col, dusk = dusk
                )
            
            out["vp"].append(vpre)
            out["time"].append(b.dn2float(tpre))
        except:
            out["vp"].append(np.nan)
            out["time"].append(np.nan)
            continue
        

    return pd.DataFrame(out, index = dates)

def join_data(df, year):
        
    infile = 'digisonde/data/PRE/saa/2014_2015_2.txt'
    df2 = b.load(infile)

    df2 = df2[df2.index.year == year]
    
    df.index = pd.to_datetime(df.index)
    ds = pd.concat([df2, df])
    
    return ds.drop_duplicates()


def run_years():
    
    out = []
    
    for year in np.arange(2013, 2023):
        
        infile = 'digisonde/data/drift/data/'
        
        fname = f'{year}_drift.txt'
        
        df = get_pre_in_year(infile + fname).dropna()
        
        if (year == 2014 ) or (year == 2015):
            
            ds = join_data(df, year).copy()
        else:
            ds = df.copy()

        out.append(ds)
        
    return pd.concat(out)
        

def join_sao_and_drift(
        year = 2014, 
        col = 'vp'
        ):
    
    drift_file = f'digisonde/data/drift/PRE/saa/{year}.txt'
    sao_file = 'digisonde/data/PRE/saa/2014_2015_2.txt'
    
    df = b.load(drift_file)[col]
    df1 = b.load(sao_file)[col]
    
    df1 = df1.loc[df1.index.year == year]
    
    ds = pd.concat([df1, df]).sort_index()
    
    return ds.groupby(ds.index).first().to_frame(col)




def replacing_values():
    
    infile = 'digisonde/data/drift/data/2022_drift.txt'
    
    df = b.load(infile)
    
    ds = b.load('pre_all_years.txt').replace(0, np.nan)
        
    ds = ds['vp'].to_frame('vp').dropna()
    
    df = dg.concat_all_pre_values().dropna()
    
    df2 = pd.concat([df, ds])
     
    df2 = df2.drop_duplicates()
    
    
    df2.to_csv('pre_all_years_2.txt')
    
    
    
# infile = 'digisonde/data/drift/data/saa/2016_drift.txt'
# infile = 'G:/Meu Drive/Python/data-analysis/digisonde/data/drift/data/saa/2016_drift.txt'
# df = get_pre_in_year(infile).dropna()

