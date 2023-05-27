import matplotlib.pyplot as plt
import pandas as pd
import settings as s
import numpy as np

def plot_profilogram(
        ax, df
        ):


    ds = pd.pivot_table(
        df, 
        index = "alt", 
        values = "freq", 
        columns = df.index
        ).interpolate()
    
    img = ax.contourf(ds.columns, ds.index, ds.values, 
                 50, cmap = "Blues")
    
    ticks = np.linspace(np.nanmin(ds.values), 
                        np.nanmax(ds.values), 10)
    s.colorbar_setting(
            img, ax, ticks, 
            label = 'Frequência (MHz)')
    
    ax.set(ylabel = "Altura (km)")


infile = "database/Digisonde/SAA0K_20130316(075).TXT"
df = pd.read_csv(infile, index_col = 0)
df.index = pd.to_datetime(df.index)
times = df.index.unique()



fig, ax = plt.subplots(
    dpi = 300,
    figsize = (12, 4)
    )

s.config_labels()

plot_profilogram(ax, df)

s.format_time_axes(
        ax, hour_locator = 12, 
        day_locator = 1, 
        tz = "UTC"
        )