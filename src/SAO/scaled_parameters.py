import datetime as dt 
import matplotlib.pyplot as plt 
import base as b 
import numpy as np 
import pandas as pd 
import spectral as sp


def plot_example(ds):
    
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (10, 5)
        )
    
    ax.plot(ds["h'F2"])
    
    ds = ds.between_time('19:00', '00:00')
    
    max_hf2 = ds["h'F2"].max()
    idx_max = ds["h'F2"].idxmax()
    
    ax.scatter(idx_max, max_hf2 )
    
    ax.set(ylabel = 'h´F2', 
           ylim = [0, 500])
    
    b.format_time_axes(
        ax, pad = 85, 
        hour_locator = 2, 
        translate = True
        )
    
    return fig
    

def dn2fl(dn):
    return dn.hour + (dn.minute/60) 


def mean_by_day(ds):
    
    ds = ds[['foF2', "h'F2", "h'F"]]
    
    ds = ds.between_time('19:00', '00:00')
    
    idx_max = ds["h'F2"].idxmax()
   
    delta = dt.timedelta(hours = 1)
    
    
    sel = ds.loc[
        (ds.index > idx_max - delta) &
        (ds.index < idx_max + delta)
        ]
    
    hF2_mean = sel["h'F2"].mean()
    foF2_mean = sel["foF2"].mean()
    
    return hF2_mean, foF2_mean, dn2fl(idx_max)

def plot_wavelet(ax, sst, time, pm = 'hF2'):
   
    wave = sp.wavelet_transform(
        sst, 
        time, 
        j1 = 2.1 
        ) 
    
    # vls = wave.power
    
    ax.contourf(
        wave.time, 
        wave.period, 
        wave.power, 
        levels = 30, 
        cmap = 'nipy_spectral'
        ) 
    
    # vmax = np.max(vls)
    # vmin = np.min(vls)
    
    # ticks = np.linspace(vmin, vmax, 10)
    # b.colorbar(img, ax, ticks = ticks, label = 'PSD')
    
    ax.set(ylabel = 'Periods (days)', 
           xlabel = 'Day of Year')

def plot_timeseries(ax, sst, time, pm = 'hF2'):
    
    ax.plot(time, sst, lw = 2)
    
    if pm == 'hF2':
        ylabel = 'h`F2 (km)'
    else:
        ylabel = 'foF2 (MHz)'
        
    ax.set(ylabel = ylabel, 
           xticks = np.arange(0, 80, 10)
           )
    
    
def get_averages_on_data():
    
    
    df = b.load('digisonde/src/SAO/test')
     
    df = df.replace(9999, np.nan)
    df = df.loc[df["h'F2"] < 999]
    
    dates = np.unique(df.index.date)
    
    out = {'hF2': [], 'foF2': [], 'tn': []}
    
    for dn in dates: 
  
        ds = df.loc[df.index.date == dn]
  
        hF2, foF2, tn = mean_by_day(ds)
        
        out['hF2'].append(hF2)
        out['foF2'].append(foF2)
        out['tn'].append(tn)
    
        
    df = pd.DataFrame(out, index = dates)
    
    df.index = pd.to_datetime(df.index)
    
    df['doy'] = df.index.day_of_year
    return df 

def plot_timeseries_and_wavelet(df):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True, 
        nrows = 2,
        ncols = 2,
        figsize = (18, 12)
        )
    
    
    plt.subplots_adjust(
        hspace = 0.05, 
        wspace = 0.3
        )
        
    sst = df['hF2'].values 
    time = df['doy'].values 
    plot_timeseries(ax[0, 0], sst, time, pm = 'hF2')
    plot_wavelet(ax[1, 0], sst, time, pm = 'hF2')
    
    sst = df['foF2'].values 
    
    plot_timeseries(ax[0, 1], sst, time, pm = 'foF2')
    plot_wavelet(ax[1, 1], sst, time, pm = 'foF2')
    

# plot_timeseries_and_wavelet(df)


df = b.load('digisonde/src/SAO/test')
 
df = df.replace(9999, np.nan)
df = df.loc[df["h'F2"] < 999]

dates = np.unique(df.index.date)

# for dn in dates:

#     ds = df.loc[df.index.date == dn]
    
#     fig = plot_example(ds)
    
#     figname = dn.strftime('%Y%m%d')
    
#     fig.savefig('E:\\ionossonde_plots\\' + figname)


df['doy'] = df.index.day_of_year + (df.index.hour / 24) + (df.index.minute / 60)

df.set_index('doy', inplace = True)


ds = df[['foF2', "h'F2"]]

# ds["h'F2"].plot()

ds = get_averages_on_data()

ds.set_index('doy', inplace = True)

del ds['tn']

ds.to_csv('juazeirinho2025.txt', sep = ' ')