import matplotlib.pyplot as plt
import pandas as pd
import settings as s
import numpy as np

def plot_frequency(
        ax, df
        ):

    ds = pd.pivot_table(
        df, 
        index = "alt", 
        values = "freq", 
        columns = df.index
        ).interpolate()
    
    img = ax.contourf(ds.columns, ds.index, ds.values, 
                 30, cmap = "rainbow")
    
    ticks = np.linspace(np.nanmin(ds.values), 
                        np.nanmax(ds.values), 6)
    s.colorbar_setting(
            img, ax, ticks, 
            label = 'Frequência (MHz)')
    
    ax.set(ylabel = "Altura (km)")
    
    
def plot_electron_density(
        ax, df
        ):
    
    df["ne"] = (1.24e4 * df["freq"]**2) * 1e6

    ds = pd.pivot_table(
        df, 
        index = "alt", 
        values = "ne", 
        columns = df.index
        ).interpolate()
    
    img = ax.contourf(ds.columns, ds.index, ds.values, 
                 30, cmap = "Blues")
    
    ticks = np.linspace(np.nanmin(ds.values), 
                        np.nanmax(ds.values), 6)
    s.colorbar_setting(
            img, ax, ticks, 
            label = 'Densidade eletrônica ($m^{-3}$)')
    
    ax.set(ylabel = "Altura (km)")


infile = "database/Digisonde/SAA0K_20130316(075).TXT"
df = pd.read_csv(infile, index_col = 0)
df.index = pd.to_datetime(df.index)
times = df.index.unique()


def plot_profilogram(df):
    fig, ax = plt.subplots(
            dpi = 300,
            sharex = True,
            sharey = True,
            nrows = 2,
            figsize = (12, 8)
    )
    
    
    plt.subplots_adjust(hspace = 0.1)
    
    s.config_labels()
    
    plot_frequency(ax[0], df)
    plot_electron_density(ax[1], df)
    s.format_time_axes(
            ax[1], hour_locator = 12, 
            day_locator = 1, 
            tz = "UTC"
    )
    
    ax[0].set(title = "Evolução temporal/altitudinal da densidade eletrônica e da frequência em São Luis")
    
    return fig
    
fig = plot_profilogram(df)


fig.savefig("digisonde/src/figures/profilogram_saa.png", dpi =300)