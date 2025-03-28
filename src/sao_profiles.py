import datetime as dt
import pandas as pd
import numpy as np
import aeronomy as io
np.seterr(divide='ignore', invalid='ignore')


def frame_from_row(row):
    value = row.split("\n")
    date_time = dt.datetime.strptime(
        value[0].strip(), 
        '%Y.%m.%d (%j) %H:%M:%S'
        )
    
    try:
        alts = [float(t) for t in value[1].split()]
        freqs = [float(t) for t in value[2].split()]
    except:
        alts = [np.nan]
        freqs = [np.nan]
    
    data = {"alt": alts, "freq": freqs}
    index = [date_time] * len(alts)
    
    return pd.DataFrame(data, index = index)
    


def process_data(infile):
    f = open(infile).read()
    
    out = []
    
    for row in f.split("\n\n"):
        try:
            out.append(frame_from_row(row))
        except:
            continue
        
    return pd.concat(out)


def load_profilogram(infile):
    df = pd.read_csv(infile, index_col = 0)
    df.index = pd.to_datetime(df.index)
    
    # compute electron density in m3
    df["ne"] = (1.24e4 * df["freq"]**2) * 1e6
    df["L"] = io.scale_gradient(df["ne"], df["alt"])
    return df


def main():
    infile = "database/Digisonde/SAA0K_20130316(075).TXT"

    df = process_data(infile)
    
    df.to_csv(infile.replace("raw", "pro"))

def run():
    import os 
    from tqdm import tqdm 
    
    infile = 'digisonde/data/jic/prof/'
    outfile = 'digisonde/data/jic/profiles/'
    
    for file in tqdm(os.listdir(infile)):
        df = process_data(infile + file)
        df.to_csv(outfile + file)

# name = 'BVJ03'
# infile = f"digisonde/data/chars/profiles/{name}_20231014(287).TXT"

# df = process_data(infile)
# path = 'digisonde/data/chars/'
# df.to_csv(path + name)

