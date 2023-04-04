import setup as p
import matplotlib.pyplot as plt
import pandas as pd
 

def plot_seasonality(infile, 
                  year = 2015):
    
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    df1 = df.loc[df.index.year == year]
    
    avg = df1.resample("15D").mean()
    std = df1.resample("15D").std()
    
    fig, ax = plt.subplots(figsize = (10, 5))
    p.config_labels()
    
    df1["vzp"].plot(marker = "o", 
                    markersize = 5,
                    linestyle = "none",
                    color = "red")
    
    ax.set(ylabel = "$V_{zp}$ (m/s)", 
           xlabel = "Meses", 
           ylim = [0, 70])
    
    ax.plot(avg["vzp"], 
            color = "k", 
            lw = 3, 
            label = "Média (15 dias)")
    
    ax.legend()
    
    ax.text(0.01, 0.9, year, transform = ax.transAxes)
    p.format_axes_date(ax)
    ax.tick_params(axis = 'x', labelrotation = 0)
    
    return fig
     
def main():
    year = 2019
    infile = f"database/drift/{year}.txt"
    plot_seasonality(infile, year = year)
    
    
