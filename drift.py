import pandas as pd
import os
from Digisonde.utils import smooth
import numpy as np
import datetime as dt


def process_day(infile, ext = "DVL"):
    
    _, _, files = next(os.walk(infile))

    files = [f for f in files if f.endswith(ext)]

    out = [load_export(os.path.join(infile, f))
           for f in files]
    
    return pd.concat(out)


def get_pre(infile):
    df = process_day(infile)
    pre = df.loc[(df.index.hour >= 18) &
                 (df.index.hour < 23), 17]
    x = pre.index
    y = pre.values
    vzp = np.max(smooth(y, 3))
    tzp = x[np.argmax(y)]
    return tzp, vzp

def process_year(root) -> pd.DataFrame:
    """
    Getting PRE values for all year
    """
    _, folders, _ = next(os.walk(root))
    
    idx = []
    out = [] 
    
    for folder in folders:
       
        try:
            print("process...", folder)
            time, vzp = get_pre(os.path.join(root, folder))
            
            idx.append(time)
            out.append(vzp)
        except:
            continue
        
    return pd.DataFrame({"vzp": out}, index = idx)

def save_df(df, year = 2015):
    
    path_to_save = f"database/drift/{year}.txt"
    df.to_csv(path_to_save, 
              sep = ",", 
              index = True)

def main():
    for year in range(2015, 2023):
        root  = f"D:\\drift\\FZA\\{year}\\"
        df = process_year(root)
        save_df(df, year = year)



def load_export(infile, smooth = False):
    
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
        
    if smooth:
        df["vx"] = smooth(df["vx"], 3)
        df["vy"] = smooth(df["vy"], 3)
        df["vz"] = smooth(df["vz"], 3)
        
    return df


def load_raw(infile, 
             date = dt.date(2013, 1, 1), 
             smooth_values = False):
    
    """
    Load process data raw (see process_year func)
    """
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    if smooth_values:
        
        for col in ["vx", "vy", "vz"]:    
            df[col] = smooth(df[col], 3)
    
    if date is not None:
        return df.loc[df.index.date == date]
    else:
        return df
    
def main():
    from build import paths as p
    infile = p("Drift").get_files_in_dir("SSA")
        
    df = load_raw(infile[0], 
                 date = dt.date(2013, 7, 19), 
                 smooth_values = True)
        
    df["vx"].plot()
