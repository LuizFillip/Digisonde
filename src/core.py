import pandas as pd
import numpy as np
    
def sel_parameter(infile, factor = "peak"):
    
    df = pd.read_csv(infile, 
                     delim_whitespace=(True), 
                     index_col = [0, 1])
    
    df = df.loc[(df.index.get_level_values('Values') ==  factor), :]
    
    df.index = pd.to_datetime(df.index.get_level_values(0))
    return df

def drift(df: pd.DataFrame) -> pd.DataFrame:
    
    """Compute the vertical drift with 
    (dh`F/dt) in meters per second"""
    
    data = df.copy()
        
    for col in data.columns:
        
        if col != "time":
        
            data[col] = (data[col].diff() / data["time"].diff()) / 3.6
    
    return data




