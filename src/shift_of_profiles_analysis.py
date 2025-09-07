import pandas as pd 
import matplotlib.pyplot as plt 
import aeronomy as io
import digisonde as dg
import core as c 
import GEO as gg 
import datetime as dt 
import base as b 

infile = 'digisonde/data/SAO/profiles/'



def profile_data(infile):
    
    df = dg.Profilegram(infile)
    
    df.index = pd.to_datetime(df.index)
    
    df["ne"] = (1.24e4 * df["freq"]**2) * 1e6
    
    df["L"] = io.scale_gradient(df["ne"], df["alt"])
    return df 

def region_E_mean(infile):
    
    df = profile_data(infile)
    
    df = df.loc[(df['alt'] > 80) & (df['alt'] < 120) ]
    
    df = df.groupby(df.index).mean()
    df.index = pd.to_datetime(df.index)
    
    return df 


def quiet_time_avg(site, p = 'ne'):
    
    files = [
        'SAA0K_20151213(347).TXT',
        'SAA0K_20151216(350).TXT', 
        'SAA0K_20151218(352).TXT', 
        'SAA0K_20151229(363).TXT'
        ]
    out = []
    for fn in files:
    
        df = region_E_mean(infile + fn)
        
        df.index = df.index.hour + df.index.minute / 60
        
        df = df.loc[~df.index.duplicated(keep='first')]
        
        out.append(df[p].to_frame())
        
    avg = pd.concat(out, axis = 1).mean(axis = 1)

    avg = c.repeat_in_stormtime(avg).to_frame('quiet')
    
    return avg 
   
def shift_quiet_storm_time(site, avg, p = 'ne'):
     
    files = [
        f'{site}_20151219(353).TXT', 
        f'{site}_20151220(354).TXT', 
        f'{site}_20151221(355).TXT', 
        f'{site}_20151222(356).TXT'
        ]
    
    out = []
    for fn in files:
        
        out.append(region_E_mean(infile + fn))
        
    df = pd.concat(out)
        
    df['quiet'] = df.index.map(avg['quiet'])
    
    df = df.resample('30min').mean()
     
    df['shift'] = ((df[p] - df['quiet']) / df['quiet']) * 100 
    
    df['shift'] = b.smooth2(df['shift'], 1)
    
    return df

def plot_span_areas(ax):

    for day in [19, 20, 21, 22]:
        if day == 20:
            color = 'red'
        else:
            color = 'gray'
        dn = dt.datetime(2015, 12, day)
        
        dusk = gg.dusk_from_site(
                dn, 
                'saa',
                twilight_angle = 18
                )
        
        delta = dt.timedelta(hours = 1)
        
        ax.axvspan(
             dusk - delta, 
             dusk + delta, 
             ymin = 0, 
             ymax = 1,
             alpha = 0.2, 
             color = color
             )
  
def plot_shift_deviation(ax, df):
    
    ax.plot(df['shift'], lw = 2)
    
    ax.axhline(0)
    
    ax.set(ylim = [-20, 20], 
           xlim = [df.index[0], df.index[-1]])
    
    b.format_time_axes(
        ax, 
        hour_locator = 12, 
        pad = 85, 
        format_date = '%d/%m/%y', 
        translate = True
        )
    
    plot_span_areas(ax)
    
        
def plot_region_E(ax, df):
    ax.plot(df[[p, 'quiet']], lw = 2)
    
    ax.set(yscale = 'log')
    
    plot_span_areas(ax)
     
def plot_shift_of_parameters(df, p):
    
    fig, ax = plt.subplots(
        figsize = (16, 10), 
        dpi = 300, 
        nrows = 2, 
        sharex= True
        )
    
    plot_region_E(ax[0], df)
    
    plot_shift_deviation(ax[-1], df)
  
    
 
    return fig
    
    
# 
site = 'FZA0M'
site = 'SAA0K'

p = 'ne'
avg = quiet_time_avg(site, p = p)

df = shift_quiet_storm_time(site, avg, p = p)

fig = plot_shift_of_parameters(df, p)