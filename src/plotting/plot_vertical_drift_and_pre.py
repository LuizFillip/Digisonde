import matplotlib.pyplot as plt
from common import sun_terminator, load, sel_dates
import settings as s
import datetime as dt
import digisonde as dg

def plot_vertical_drift_and_pre(ds):
    
    fig, ax = plt.subplots(
        figsize = (10, 5),
        dpi = 300)
    
    ax.plot(ds["vz"], label = "Vz")
    
    ax.axhline(0, linestyle = "--")
    ax.set(xlim = [ds.index[0], ds.index[-1]])
    s.format_time_axes(ax)
    ax.set(ylabel = "Deriva vertical (m/s)", 
           xlim = [ds.index[0], ds.index[-1]], 
           ylim = [-75, 75])
    
    ax.legend(loc = "upper left")
    
    return fig


dn = dt.datetime(2014, 1, 3, 18)
delta = dt.timedelta(hours = 10)

infile = 'database/Digisonde/process/SL_2014-2015/mean_hf.txt'

df = dg.get_drift(load(infile))

df = sel_dates(df, start = dn, end = dn + delta)

plot_vertical_drift_and_pre(df)