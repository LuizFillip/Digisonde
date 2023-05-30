import numpy as np
import pandas as pd



def pro_characteristics(infile):
    f = open(infile).readlines()
    
    raw_data = [f[i].split() for i 
                in range(2, len(f))]
        
    colums = ["date", "doy", "time", 
              'foF2', 'h`F2', 'QF', 
              'hmF2', 'f(hF2)']
    
    df = pd.DataFrame(raw_data, columns = colums)
    
    df.index = pd.to_datetime(
        df["date"] + " " + df["time"]
        )
    
    df.drop(columns = colums[:3], inplace = True)
    
    df = df.replace("---", np.nan)
    
    for col in df.columns:
        df[col] = pd.to_numeric(df[col])
    
    return df.interpolate()

def main():
    infile = "database/Digisonde/SAA0K_20130316(075)_cha"
    
    df = pro_characteristics(infile)
    
  

