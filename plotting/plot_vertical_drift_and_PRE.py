from RayleighTaylor.src.common import get_pre, load
import matplotlib.pyplot as plt
import numpy as np
import setup as s
from Results.utils import get_dusk
import datetime as dt
      
  

def plot_drift_part(ax, df, dn):
    
    ax.plot(df["vz"], color = "k")
    
    tpre, vpre = get_pre(dn, df)
    
    ax.axvline(
        tpre, color = "k", 
        linestyle = "--",
        label = f"Vzp = {vpre} m/s ({tpre.time()} UT)"
               )
    sunset, dusk = get_dusk(dn)

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
    
    
ts = load()
df = ts.drift()

dates = np.unique(df.index.date)
dn = dates[0]
df = df.loc[df.index.date == dn]
x, y = get_pre(dn, df)

fig, ax = plt.subplots(figsize = (8, 4))

plot_drift_part(ax, df, dn)



