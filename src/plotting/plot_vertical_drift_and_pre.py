import matplotlib.pyplot as plt
from common import sun_terminator, load, sel_dates
import settings as s
import datetime as dt
import digisonde as dg
import numpy as np
import pandas as pd

def plot_vertical_drift_and_pre(ds, dn):
    
    fig, ax = plt.subplots(
        figsize = (10, 5),
        dpi = 300)
    
    ax.plot(ds["vz"])
    
    ax.axhline(0, linestyle = "--")
    
    
    ax.set(ylabel = "Deriva vertical (m/s)", 
           xlim = [ds.index[0], ds.index[-1]], 
           ylim = [-75, 75])
    
    t, p = ds['vz'].idxmax(), ds['vz'].max()
    
    ax.scatter(t, p)
    
    colors = ['b', 'r', 'k']
    labels = [0, 125, 300]
    for i, angle in enumerate([0, 12, 18]):
        ax.axvline(sun_terminator(
            dn, 
            twilight_angle = angle), 
            color = colors[i],
            label = f'{labels[i]} km'
            )
        
    ax.legend(loc = "upper left")
    s.format_time_axes(ax)
    return fig

def save_plots():
    from utils import dn2FigureName, save_img

    infile = 'database/Digisonde/process/SL_2014-2015/mean_hf.txt'
    
    df = dg.get_drift(load(infile))
    
    
    save_in = 'D:\\plots2\\PRE\\'
    
    for dn in np.unique(df.index.date):
        
        dn = pd.to_datetime(dn)
        start = dn + dt.timedelta(hours = 18)
        ds = sel_dates(
            df, 
            start = start, 
            end = start + dt.timedelta(hours = 8)
            )
        
        try:
            f = plot_vertical_drift_and_pre(ds, dn)
            
            save_img(f, save_in + dn2FigureName(dn))
        except:
            continue