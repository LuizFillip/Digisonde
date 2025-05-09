import pandas as pd
import os
from tqdm import tqdm

def load_export(infile):
    
    """
    Vz: Vertical component (positive to up)
    Vx: Meridional component (positive to north)
    Vy: Zonal component (positive to east)
    """
    
    df = pd.read_csv(
        infile, 
        delim_whitespace = True, 
        header = None
        )
    
    try:
        
        df.index = pd.to_datetime(df[5] + " " + df[7])
        
        df.drop(columns = list(
            range(8)) + list(range(18, 23)), 
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


def process_day(infile, ext = "DVL"):
    
    
   files = [f for f in os.listdir(infile) if f.endswith(ext)]
   
   out = [load_export(
       os.path.join(infile, filename)
       ) for filename in files]
  
   return  pd.concat(out)

def process_year(main_path):

    
    files = os.listdir(main_path)
    
    out = []
    
    for folder in tqdm(files):
            
        try:
            out.append(process_day(
                os.path.join(main_path, folder))
                )
        except:
            continue
    return pd.concat(out)



site = 'saa'
year = 2023

def process_drift(year, site):
    path = f'D:\\drift\\{site}\\{year}\\'
    df = process_year(path)
    save_in = f'digisonde/data/drift/data/{site}/{year}_drift.txt'
    df.to_csv(save_in)