import pandas as pd
import os
from tqdm import tqdm
# import matplotlib.pyplot as plt
# import datetime as dt
import base as b 

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
    finfile = 'D:\\drift\\JIC\\2017\\'

    files = os.listdir(infile)

    out = []
    date = []
    for fname in files:
        
        try:
            df = load_export(infile + fname)
            df['vz'] = b.smooth2(df['vz'], 5)
            
            dn = pd.to_datetime(
                df.index[0].date(
                    ))
            
            ds = b.sel_times(df, dn, hours = 1.5)
            
            out.append(ds['vz'].max())
            date.append(dn)
                
        except:
            continue
        
        
    plt.scatter(date, out)

    
    


# ds['vz'].plot()