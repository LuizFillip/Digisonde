import datetime as dt 
import matplotlib.pyplot as plt 
import base as b 
import numpy as np 
import pandas as pd 

def plot_example(ds, pm = "h'F2"):
    
    max_hf2 = ds[pm].max()
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (10, 5)
        )
    
    ax.plot(ds[pm])
    
    # ax.scatter(idx_max, max_hf2 )
    # ax.scatter(idx_max, hF2_mean )
    
    b.format_time_axes(
        ax, pad = 85, 
        hour_locator = 2, 
        translate = True
        )
    
    


def mean_by_day(ds):
    
    ds = ds.interpolate()
    
    pm = "h'F2"
    
    ds[pm] = b.running(ds[pm], 2)
    
    
    idx_max = ds[pm].idxmax()
   
    
    delta = dt.timedelta(hours = 1)
    
    sel = ds.loc[
        (ds.index > idx_max - delta) &
        (ds.index < idx_max + delta)
        ]
    
    hF2_mean = sel[pm].mean()
    foF2_mean = sel["foF2"].mean()
    
    return  hF2_mean, foF2_mean


df = b.load('digisonde/src/SAO/test')


df = df.replace(9999, np.nan)
df = df.loc[df["h'F2"] < 999]


dates = np.unique(df.index.date)

out = {'hF2': [], 'foF2': []}

for dn in dates: 
    
    ds = df.loc[df.index.date == dn]

    hF2, foF2 = mean_by_day(ds)
    
    out['hF2'].append(hF2)
    out['foF2'].append(foF2)
    
    
df = pd.DataFrame(out, index = dates)

df['hF2'].plot() 