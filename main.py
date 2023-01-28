import os
from core import iono_frame
from tqdm import tqdm 
from PRE import pre
import pandas as pd


def run_for_all_files(infile):
    _, _, files = next(os.walk(infile))
    
    out = []
    for filename in files:
        days = iono_frame(infile + filename).days
        for day in tqdm(days, desc = filename):
            try:
                out.append(pre(infile, filename, day = day))
            except:
                continue

    return pd.concat(out)           

def compute_pre(station = "SL", save = True):
    
    
    infile = f"database/process/{station}_2014-2015/"
    
    df = run_for_all_files(infile)
    
    if save:
        df.to_csv(f"database/vzp/{station}_PRE_2014_2015.txt", 
                  sep = ",", 
                  index = True)
    return df
