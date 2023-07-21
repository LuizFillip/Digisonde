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
    
    
   files = [f for f in tqdm(os.listdir(infile)) 
            if f.endswith(ext)]
   
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

def run_years():
    for year in range(2016, 2023):
    
        main_path = f'D:\\drift\\SAA\\{year}\\'
        
        try:
            
            df = process_day(main_path)
        except:
            df = process_year(main_path)
        
        df.to_csv(f'{year}_drift.txt')
    
    
# run_years()