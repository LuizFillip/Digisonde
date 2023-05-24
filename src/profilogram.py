import datetime as dt
import pandas as pd
import numpy as np





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
    
infile = "database/Digisonde/SAA0K_20130917(260).TXT"


def process_data(infile):
    f = open(infile).read()
    
    out = []
    
    for row in f.split("\n\n"):
        try:
            out.append(frame_from_row(row))
        except:
            continue
        
    return pd.concat(out)


df = process_data(infile)

df.to_csv("iono_freqs.txt")