import numpy as np
import pandas as pd



def pipeline_char(infile):
    f = open(infile).readlines()
    
    raw_data = [f[i].split() for i 
                in range(2, len(f))]
        
    colums = [
        "date", "doy", "time", 
              'foF2', 'hF2', 'QF', 
              'hmF2', 'f(hF)', 'f(hF2)']
    
    df = pd.DataFrame(
        raw_data, 
        columns = colums)
    
    df.index = pd.to_datetime(
        df["date"] + " " + df["time"]
        )
    
    df.drop(
        columns = colums[:3], 
        inplace = True
        )
    
    df = df.replace("---", np.nan)
    
    for col in df.columns:
        df[col] = pd.to_numeric(df[col])
    
    return df

def main():
    infile = "database/Digisonde/SAA0K_20130316(075)_cha_raw"
    
    df = pipeline_char(infile)
    df.to_csv(infile)
  


