import pandas as pd
import numpy as np
import datetime as dt


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

