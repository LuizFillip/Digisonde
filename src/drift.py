import pandas as pd
import os
import numpy as np
import datetime as dt




def get_pre(dn, df):
    
    b = dt.time(21, 0, 0)
    e = dt.time(22, 30, 0)
    
    df = df.loc[(df.index.time >= b) & 
                (df.index.time <= e) & 
                (df.index.date == dn), ["vz"]]
        
    return df.idxmax().item(), round(df.max().item(), 2)

def get_pre_in_year(df):
        
    dates = pd.date_range("2013-1-1", "2013-12-31", freq = "1D")
    
    out = {"vp": [], "time": []}
    
    for dn in dates:
        
        try:
            df1 = df.loc[df.index.date == dn.date()]
            tpre, vpre = get_pre(dn.date(), df1)
            
            out["vp"].append(vpre)
            out["time"].append(tpre)
        except:
            out["vp"].append(np.nan)
            out["time"].append(np.nan)
            continue
        
        
    ds = pd.DataFrame(out, index = dates)
    
    
    
    return ds

def filter_error_vls(ds):
    ds.loc[(ds.index.month <= 4) 
           & (ds["vp"] < 10), "vp"] = np.nan
    
    ds.loc[ (ds.index.month > 9)
           & (ds["vp"] < 10), "vp"] = np.nan
    return ds


def load_export(infile):
    
    """
    Vz: Vertical component (positive to up)
    Vx: Meridional component (positive to north)
    Vy: Zonal component (positive to east)
    """
    
    df = pd.read_csv(infile, 
                     delim_whitespace = True, 
                     header = None)
    
    try:
        
        df.index = pd.to_datetime(df[5] + " " + df[7])
        
        df.drop(columns = list(range(8)) + list(range(18, 23)), 
                inplace = True)
    except:
        
        df.index = pd.to_datetime(df[6] + " " + df[8])
        
        df.drop(columns = (list(range(9)) + 
                           list(range(19, 24))), 
                inplace = True)
        
        
    names = ["vx", "evx", "vy", "evy",  
             "az", "eaz", "vh", "evh",
             "vz", "evz"]
    
    for num, name in enumerate(df.columns):
        df.rename(columns = {name: names[num]}, 
                  inplace = True)
        
    return df

def process_day(infile, 
                ext = "DVL", 
                save_in = "20131.txt"):
    
    
   files = os.listdir(infile)
   files = [f for f in files if f.endswith(ext)]
   out = []
   for filename in files:
       
       try:
           out.append(load_export(infile + filename))
       except:
           print(filename)
           continue
   df = pd.concat(out)
   
   df.to_csv(save_in, index = True)
   
   return df




