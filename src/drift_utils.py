import pandas as pd
import numpy as np
from utils import smooth2, time2float


def get_avg_std(df, only_values = True):
    
    avg = df.mean(axis = 1)
    std = df.std(axis = 1)
    
    if only_values:
        return (avg.values, std.values)
    else:
        return avg, std

def filter_values(df, 
                  std_factor = 1, 
                  replace_nan = True):
    
    """df must be pivot table (time x date)"""
    
    avg, std = get_avg_std(df)
    
    out = []
       
    for col in df.columns:
        
        arr = df[col].values
        right = avg + (std_factor * std)
        left = avg - (std_factor * std)
    
        res = np.where((arr < right) & 
                       (arr > left), 
                       arr, 
                       np.nan)
        
        out.append(pd.DataFrame({col: res}, 
                                index = df.index))
        
    df = pd.concat(out, axis = 1)    
    if replace_nan:
        
        df["avg"] = avg
        for col in df.columns:
            df.loc[df[col].isnull(), col] = df['avg']
            
        del df["avg"]
        return df
    else:
        return df


def pivot_data(n, col, 
               smoothed = True, 
               resample = True):

    df = load_drift(n, 
                    smoothed = smoothed, 
                    resample = resample)
    
   
    df["time"] = time2float(df.index.time)
    
    
    return pd.pivot_table(
        df, 
        values = col, 
        columns = df.index.date, 
        index = "time"
        )

def reindex_and_concat(df, name):

    out = []
    
    for col in df.columns:
    
        idx = pd.date_range(f"{col}", 
                            freq = "5min", 
                            periods = len(df))
        
        new_df = df[col]
        
        new_df.index = idx
        
        out.append(new_df.to_frame(name = name))
        
    return pd.concat(out)


def process_year(name):
    out = []
    
    for n in range(1, 13, 1):
        print("processing...", n, name)
        df = pivot_data(n, smoothed = True, col = name)
        df_filtered = filter_values(df, std_factor = 1)
        
        out.append(reindex_and_concat(
            df_filtered, name))
    
    return pd.concat(out)



    

    

infile = "database/Drift/SSA/PRO_2013.txt"





def sampled(ds, freq = "2min"):
    
    sts = ds.index[0].date()
    end = ds.index[-1].date()
    
    df1 = pd.DataFrame(
        index = pd.date_range(
            f"{sts} 00:02", 
            f"{end} 23:58", 
            freq = freq
    ))
    
    ds = pd.concat( [ds, df1], axis = 1
                   ).interpolate().bfill()
    return ds.resample(freq).asfreq()


def load_drift(infile, freq = "2min"):
    
    df = pd.read_csv(infile, index_col = 0)

    df.index = pd.to_datetime(df.index)

    df["vz"] = smooth2(df["vz"], 3)
    
    return sampled(df, freq = freq)

# load_drift(infile, freq = "2min")