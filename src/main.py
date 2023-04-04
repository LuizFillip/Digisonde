import os
from tqdm import tqdm 
import pandas as pd
from Digisonde.drift import load_export
from build import paths as p
from Digisonde.drift_utils import process_year



def concat_files_and_save(infile,
                          ext = "DVL", 
                          filename = "2015.txt") -> str:
    #infile = "database/Drift/RAW/"
    files = os.listdir(infile)
    files = [f for f in files if f.endswith(ext)]
    out = []
    for filename in tqdm(files, 
                         desc = "run"):
        try:
            f = open(infile + filename, "r")
            out.append(f.read())
        except:
            continue
        
    res = "".join(out)
    
    text_file = open(filename, "w")
    text_file.write(res)
    text_file.close()
    return res

def concat_files(site = "SSA_PRO", 
                 save = True, 
                 year = 2015):
    
    """
    load and concat all files prosseced 
    by DRIFT - X
    """

    f = p("Drift")
    
    files = f.get_files_in_dir(site)
    out = []
    for filename in tqdm(files, desc = "running"):
        out.append(load_export(filename))
    
    df = pd.concat(out).sort_index()
    
    if save:
        #filename variable missing
        to_save = os.path.join(f.root, f"{year}.txt") 
        df.to_csv(to_save, index = True)
        
    return df

    
def process_dirs():
    out = []
    for name in ["vy", "vx", "vz"]:
        out.append(process_year(name))
        
    ts = pd.concat(out, axis = 1)
    
    f = p("Drift").get_dir("REDUCED")
    
    ts.to_csv(os.path.join(f, "2013.txt"))
    return ts


def main():
    
    infile ="database/Drift/FZA/RAW_2016.txt"

    df = load_export(infile)

    print(df.to_csv(infile, index = True))
    
#main()