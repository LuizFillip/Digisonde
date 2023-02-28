import pandas as pd
import os
from Digisonde.utils import smooth
import numpy as np
from build import paths as p

def process_day(infile, 
                ext = "DVL", 
                save_in = "2015.txt"):
    
    
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


def load_DRIFT(smooth = False):
    infile = p("Drift").get_files_in_dir("REDUCED")
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    if smooth:
        df["vx"] = smooth(df["vx"], 3)
        df["vy"] = smooth(df["vy"], 3)
        df["vz"] = smooth(df["vz"], 3)
    return df

