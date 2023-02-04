import pandas as pd
import os
from utils import smooth
import numpy as np

def load(infile):

    df = pd.read_csv(infile, 
                     delim_whitespace = True, 
                     header = None)
    
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

def process_day(infile):
    
    _, _, files = next(os.walk(infile))

    files = [f for f in files if f.endswith("DVL")]

    out = [load(os.path.join(infile, f))
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
    
    if year:
        path_to_save = f"database/drift/{year}.txt"
    else:
        path_to_save = f"database/drift/{year}.txt"
    df.to_csv(path_to_save, 
              sep = ",", 
              index = True)

def main():
    for year in range(2015, 2023):
        root  = f"D:\\drift\\FZA\\{year}\\"
        df = process_year(root)
        save_df(df, year = year)



    
