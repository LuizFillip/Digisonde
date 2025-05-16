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
    


def Profilegram(infile):
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


def storm_profiles(site = 'FZA0M'):
    
    path_profiles = 'digisonde/data/SAO/profiles/'
    
    files = [
        f'{site}_20151219(353).TXT', 
        f'{site}_20151220(354).TXT', 
        f'{site}_20151221(355).TXT', 
        f'{site}_20151222(356).TXT'
        ]
    
    out = []
    
    for fn in files:
        infile = path_profiles + fn 
        
        out.append(Profilegram(infile))
        
    df = pd.concat(out)
    
    df["ne"] = (1.24e4 * df["freq"]**2) * 1e6
    df["L"] = io.scale_gradient(df["ne"], df["alt"])
    
    return df 


# 