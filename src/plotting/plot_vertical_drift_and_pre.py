import os
import matplotlib.pyplot as plt
import RayleighTaylor as rt
from common import plot_terminators
import settings as s
from utils import save_but_not_show, fname_to_save



def plot_vertical_drift_and_pre(ds):
    
    fig, ax = plt.subplots(
        figsize = (10, 5),
        dpi = 300)
    
    ax.plot(ds[["vzp", "vz"]])
    
    ax.axhline(0, linestyle = "--")
    ax.set(xlim = [ds.index[0], ds.index[-1]])
    s.format_time_axes(ax)
    ax.set(ylabel = "Deriva vertical (m/s)", 
           xlim = [ds.index[0], ds.index[-1]], 
           ylim = [-75, 75])
    
    ax.legend(["Vzp", "Vz"], loc = "upper left")
    
    plot_terminators(ax, ds)
    
    fig.suptitle("Varição diária da deriva vertical (DRIFT-X)")
    
    return fig


def save():
    
    save_in = "D:\\plots\\parameters\\drift\\"
        
    infile = "database/RayleighTaylor/reduced/300.txt"
    df = rt.load_process(infile, apex = 300)
    
    for ds in rt.split_by_freq(df, freq_per_split = "10D"):
        
        name_to_save = fname_to_save(ds)
        
        dn = ds.index[0]
        print("saving...", name_to_save)
        
        fig = plot_vertical_drift_and_pre(ds)
        
        month_name = dn.strftime("%m")
                
        save_it = os.path.join(
            save_in, month_name, name_to_save 
            )
        save_but_not_show(fig, save_it)
        
save()
        

def main():
    infile = "database/RayleighTaylor/reduced/300.txt"
    df = rt.load_process(infile, apex = 300)
    
    ds = rt.split_by_freq(df, freq_per_split = "10D")[0]
    
    fig = plot_vertical_drift_and_pre(ds)
    plt.show()