import pandas as pd 
import matplotlib.pyplot as plt 
import aeronomy as io
import digisonde as dg
import core as c 
import GEO as gg 
import datetime as dt 
import base as b 

infile = 'digisonde/data/SAO/profiles/'

files = [
    'SAA0K_20151213(347).TXT',
    'SAA0K_20151216(350).TXT', 
    'SAA0K_20151218(352).TXT', 
    'SAA0K_20151229(363).TXT'
    ]

def profile_data(infile):
    
    df = dg.Profilegram(infile)
    
    df.index = pd.to_datetime(df.index)
    
    df["ne"] = (1.24e4 * df["freq"]**2) * 1e6
    
    df["L"] = io.scale_gradient(df["ne"], df["alt"])
    return df 

def region_E_mean(infile):
    
    df = profile_data(infile)
    
    df = df.loc[(df['alt'] > 80) & (df['alt'] < 150) ]
    
    df = df.groupby(df.index).mean()
    df.index = pd.to_datetime(df.index)
    
    return df 



p = 'ne'
out = []
for fn in files:

    df = region_E_mean(infile + fn)
    
    df.index = df.index.hour + df.index.minute / 60
    
    df = df.loc[~df.index.duplicated(keep='first')]
    
    out.append(df[p].to_frame())
    
avg = pd.concat(out, axis = 1).mean(axis = 1)


avg = c.repeat_in_stormtime(avg).to_frame('quiet')



fn = 'SAA0K_20151219(353).TXT'



df = region_E_mean(infile + fn) 



df['quiet'] = df.index.map(avg['quiet'])

df = df.resample('30min').mean()


df['shift'] = ((df[p] - df['quiet']) / df['quiet']) * 100 

df['shift'] = b.smooth2(df['shift'], 2)

def plot_shift_of_parameters(df):
    
    fig, ax = plt.subplots(
        figsize = (12, 6), 
        dpi = 300
        )
    
    
    ax.plot(df['shift'])
    
    ax.axhline(0)
      
    ax.set(xlim = [df.index[0], df.index[-1]])
    
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
    
    ax.set(ylim = [-20, 20])
    
    b.format_time_axes(
        ax, hour_locator = 12, pad = 85, 
    format_date = '%d/%m/%y', 
    translate = True)
    
    
plot_shift_of_parameters(df)