import matplotlib.pyplot as plt
from build import paths as p
from Digisonde.drift import load_raw
import datetime as dt
import setup as s



def plotDRIFTComponents(ts):
    
    """
    Vz: Vertical component (positive to up)
    Vx: Meridional component (positive to north)
    Vy: Zonal component (positive to east)
    """

    fig, ax = plt.subplots(nrows = 3, 
                           sharex = True, 
                           figsize = (12, 10))
    
    plt.subplots_adjust(hspace = 0.2)
    s.config_labels()
    
    date = ts.index[0].strftime("%d de %B de %Y")
    
    args = dict(marker = "o", 
                linestyle = "none", 
                markersize = 5, 
                color = "k", 
                fillstyle = "none",
                capsize = 3)
    
    ts["vz"].plot(ax = ax[0], yerr = ts["evz"], **args)
    ts["vx"].plot(ax = ax[1], yerr = ts["evx"], **args)
    ts["vy"].plot(ax = ax[2], yerr = ts["evy"], **args)
    
    li = [ 50, 150, 150]
    na = ["vertical", "meridional", "zonal"]
    
    for n, ax in enumerate(ax.flat):
        
        ax.axhline(0, color = "red")
        
        ax.set(ylim = [-li[n], li[n]], 
               xlim = [ts.index[0], 
                       ts.index[-1]], 
               ylabel = f"Velocidade (m/s)")
        
        ax.grid()
        
        ax.text(0, 1.04, "Componente " + na[n], 
                transform = ax.transAxes)
        
        s.format_axes_date(ax, time_scale = "hour")
        
        if n == 2:
            ax.set(xlabel = "Hora universal (UT)")
    
    fig.autofmt_xdate(rotation=0, ha = 'center')
    fig.suptitle(date, y = 0.91)


infile = p("Drift").get_files_in_dir("SSA")

    
ts = load_raw(infile[0], 
             date = dt.date(2013, 7, 19), 
             smooth_values = True)
    
plotDRIFTComponents(ts)