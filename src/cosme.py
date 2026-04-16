import pandas as pd
import aeronomy as ae 
import digisonde as dg 
from models import timerange_msis, correct_and_smooth
import base as b 
import datetime as dt 
import matplotlib.pyplot as plt 

def drift():
    file = 'database/cosme/contours'
     
    ds = dg.freq_fixed(file)
    
    ds = dg.calc_drift(ds, sf = None, smooth = 5)
    
    return ds['vz']

 
def gravity(alt = 300):
    times = pd.date_range(
        '2015-09-17 19:00', 
        '2015-09-18 07:00',
        freq = '10min'
        )
    df = timerange_msis(
            times, 
            site = "fza", 
            altitude = alt 
            )
     
    nu = ae.collision_frequencies()
    
    df["nui"] = nu.ion_neutrals(
        df["Tn"],
        df["O"], 
        df["O2"], 
        df["N2"]
        )
    
    df['vr'] = (5.15e-13 * df['N2']) + (1.2e-11 * df['O2'])
     
    smoothed, corrected, slip_idx = correct_and_smooth(df['nui'])
    
    df['nui'] = smoothed
    
    df['gr'] = 9.8 / df['nui']
    
    return df[['gr', 'vr']]

def gradient():
    infile = 'database/cosme/profiles'
    
    df = dg.Profilegram(infile)
    
    df["ne"] = (1.24e4 * df["freq"]**2) * 1e6
    df["L"] = ae.scale_gradient(df["ne"], df["alt"])
    
    df = df.loc[df['alt'] == 300]
    
    df['L'] = df['L'].rolling(
            window=5,
            center=True,
            min_periods=1
        ).mean()

    return df['L']


df = pd.concat(
    [gradient(), gravity(), drift()], axis =1 
    )

 
df = df.interpolate()


df['gamma'] = df['L'] * (df['gr'] + df['vz'])  - df['vr']

def plot_gamma():
    b.sci_format()
    fig, ax = plt.subplots(
        figsize = (12, 4), dpi = 300
        )
    
    ax.plot(df['gamma'] * 1e3)
    
    ref_day = dt.datetime(2015, 9, 18, 2)
    ax.axvspan(
         ref_day, 
         ref_day + dt.timedelta(hours = 2), 
         ymin = 0, 
         ymax = 1,
         alpha = 0.2, 
         color = 'gray'
         )
    
    ax.set(ylabel = '$\\gamma_{RT}$ (1e3 s$^{-1}$)')
    ax.axhline(0, linestyle = ':')
    
    b.format_time_axes(ax, translate = True)