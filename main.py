import os
from core import iono_frame
from tqdm import tqdm 
from PRE import pre
import pandas as pd
from Digisonde.drift import load_export
from build import paths as p

def concat_files(site = "SSA_PRO", 
                 save = True):
    
    """
    load and concat all files prosseced 
    by DRIFT - X
    """

    f = p("Drift")
    
    files = f.get_files_in_dir(site)
    out = []
    for filename in files:
        out.append(load_export(filename))
    
    df = pd.concat(out).sort_index()
    
    if save:
        #filename variable missing
        to_save = os.path.join(f.root,
                               site[:3], 
                               "PRO_2013.txt") 

        df.to_csv(to_save, index = True)
        
    return df

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


def join_drift_files(root,
                     year = 2013, 
                     site = "SAA", 
                     save = True):
    
    base = f"{root}{site}\\{year}\\"
    _, folders, _ = next(os.walk(base))
    
    from drift import process_day
    
    out = []
    
    for folder in folders:
        try:
            print("process...", folder)
            out.append(process_day(os.path.join(base, folder)))
        except:
            continue
    
    df = pd.concat(out)
    
    if save:
    
        df.to_csv(f"{year}_raw.txt", 
                  index = True)
    return df

    
