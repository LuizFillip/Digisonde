from RayleighTaylor.src.common import get_pre, load
import matplotlib.pyplot as plt
import numpy as np
import setup as s
from Results.utils import get_dusk
import datetime as dt
from AllSky.labeling import save_img

  

def plot_drift_part(ax, df, dn):
    
    ax.plot(df["vz"], color = "k")
    
    tpre, vpre = get_pre(dn, df)
    
    ax.axvline(
        tpre, color = "k", 
        linestyle = "--",
        label = f"Vzp = {vpre} m/s ({tpre.time()} UT)"
               )
    
    sunset, dusk = get_dusk(dn, lat = -2.53, lon = -44.296)

    ax.axvline(sunset, label = "0 km")
    ax.axvline(dusk,  label = "300 km", color = 'r')

    ax.legend(loc = "upper left")
    ax.grid()
    
    s.format_axes_date(ax, time_scale = "hour", interval = 4)
    
    ax.set(xlabel = "Hora universal",
        ylim = [-50, 50], 
        title = dn,
        ylabel = r"$V_z ~ (ms^{-1})$"
        )
    
    

def save_all_figs():

    ts = load()
    df = ts.drift()
    
    dates = np.unique(df.index.date)
    for dn in dates:
        
        df1 = df.loc[df.index.date == dn]
        
        fig, ax = plt.subplots(figsize = (8, 4))
        
        save_in = "D:\\drift\\SAA-plots\\"
        
        plot_drift_part(ax, df1, dn)
        
        filename  = dn.strftime("%Y%m%d") + ".png"
        print("saving...", filename)
        save_img(fig, save_in + filename)
    

save_all_figs()
