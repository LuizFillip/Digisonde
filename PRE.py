import pandas as pd
import numpy as np
from time_terminators import time_to_float, terminators
from core import iono_frame
import os
from tqdm import tqdm 

def drift(df: pd.DataFrame) -> pd.DataFrame:
    
    """Compute the vertical drift with 
    (dh`F/dt) in meters per second"""
    
    data = df.copy()
        
    for col in data.columns:
        
        if col != "time":
        
            data[col] = (data[col].diff() / data["time"].diff()) / 3.6
    
    return data

def get_values(infile, filename, day):
    df = pre(infile, 
             filename, 
             day = day)
    
    peak = df.iloc[(df.index.get_level_values('Values') == 
                            "peak"), :].values[0]
    
    time = df.iloc[(df.index.get_level_values('Values') == 
                            "time"), :].values[0]

    return (peak, time)

def find_maximus(df):
    """Get maximus for """
    result = {}

    pre = df.max().values
    times = df.idxmax().values
    
    for num, col in enumerate(df.columns[1:]):
        
        num = num + 1
        
        intime = pd.to_datetime(times[num])
           
        result[col] = list((time_to_float(intime), 
                            round(pre[num], 3)))
        
    return result


def pre(infile: str, 
        filename: str, 
        day: int = 2) -> pd.DataFrame:    

    
    df = iono_frame(infile + filename).sel_day_in(day = day)
    date = df.index[0].date()
    t = terminators(filename, date = date)


    vz = drift(df)

    set_vz = vz.loc[((vz.time > t.sunset) & 
                     (vz.time < t.dusk)), :]
   
    dat = find_maximus(set_vz)


    vzp = np.array([dat[num][1] for num in dat.keys()]).mean()
    vzt = np.array([dat[num][0] for num in dat.keys()]).mean()
    
    return pd.DataFrame({"vz": vzp, "time": vzt}, index = [date])


def all_frequencies(df):
    
    day = pd.to_datetime(df.index[0]).strftime('%Y-%m-%d')
    
    dat = find_maximus(df)
    
    tuples = list(zip([day, day], ["time", 
                                   "peak"]))
    
    index = pd.MultiIndex.from_tuples(tuples, 
                                      names=["date", 
                                             "values"])
    return pd.DataFrame(dat, index = index) 


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

def main():
    
    station = "SL"
    infile = f"database/process/{station}_2014-2015/"
    
    df = run_for_all_files(infile)
    
    df.to_csv(f"database/vzp/{station}_PRE_2014_2015.txt", 
              sep = ",", 
              index = True)
    print(df)

#main()