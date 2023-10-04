import os
import digisonde as dg
import pandas as pd

infile = 'database/jic/freq/'

def run_pre():

    site = 'jic'
    out = []
    
    for f in os.listdir(infile):
        out.append(dg.PRE_from_SAO(infile + f, site))
        
    return pd.concat(out)

