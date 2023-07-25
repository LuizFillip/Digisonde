import pandas as pd
import numpy as np
import digisonde as dg
import datetime as dt
from base import sun_terminator, load_by_time, sel_dates
from base import smooth2, dn2float

def get_drift(df, col = 'hf'):
    
    df[col] = df[col].interpolate()
    
    df['vz'] = (df[col].diff() / 
               df["time"].diff()) / 3.6
    
    df['vz'] = smooth2(df['vz'], 5)
    
    return df

def vertical_drift(
        df: pd.DataFrame, 
        sel_columns = None
        ) -> pd.DataFrame:
    
    """
    Compute the vertical drift with 
    (dh`F/dt) from ionosonde fixed frequency 
    (in meters per second)
    """
    
    data = df.copy()
    
    if sel_columns is not None:
        columns = data.columns
    else:
        columns = sel_columns
        
    for col in columns:
        
        if col != "time":
        
            data[col] = (data[col].diff() / 
                         data["time"].diff()) / 3.6

    data["avg"] = np.mean(data[columns[1:]], axis = 1)
    return data


def sel_between_terminators(df, dn):
    
    dn = pd.to_datetime(dn)
    start = sun_terminator(dn, twilight_angle = 0)
    end = sun_terminator(dn, twilight_angle = 18)
    
    return sel_dates(df, start = start, end = end)



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
        df, 
        col = 'vz', 
        dusk = True
        ):
      
    out = {"vp": [], "time": []}
    
    dates = np.unique(df.index.date)
    
    for dn in dates:
         
        try:
            ds = df.loc[df.index.date == dn]
            tpre, vpre = get_pre(
                dn, ds, col = col, dusk = dusk
                )
            
            out["vp"].append(vpre)
            out["time"].append(dn2float(tpre))
        except:
            out["vp"].append(np.nan)
            out["time"].append(np.nan)
            continue
        

    return pd.DataFrame(out, index = dates)




def add_vzp(
        infile = "database/Digisonde/SAA0K_20130216_freq.txt"
        ):

    df = load_by_time(infile)
    vz = dg.drift(
        df, 
        sel_columns = [6, 7, 8]
        )
    
    out = {"idx": [], "vzp": []}
    for dn in np.unique(vz.index.date):
        idx, vzp = get_pre(dn, vz)
        out["idx"].append(idx.date())
        out["vzp"].append(vzp)
        
    return pd.DataFrame(out).set_index("idx")


def run_years():
    
    for year in [2013, 2014, 2015]:
        infile = f'{year}_drift.txt'
        df = load_by_time(infile)
        
        df['vz'] = smooth2(df['vz'], 5)
    
            
        ds = get_pre_in_year(df)
        
        save_in = 'database/Drift/PRE/SAA/'
        ds.to_csv(save_in + f'{year}_2.txt')
    

    # infile = 'database/Digisonde/process/SL_2014-2015/mean_hf.txt'
    
    # df = get_drift(load_by_time(infile))
    
    # ds = get_pre_in_year(
    #         df, 
    #         col = 'vz', 
    #         dusk = True
    #         )
# run_years()