import digisonde as dg
import RayleighTaylor as rt
from utils import fname_to_save, save_but_not_show
import os


def save():
    
    save_in = "D:\\plots\\parameters\\drift\\"
        
    infile = "database/RayleighTaylor/reduced/300.txt"
    df = rt.load_process(infile, apex = 300)
    
    for ds in rt.split_by_freq(df, freq_per_split = "10D"):
        
        name_to_save = fname_to_save(ds)
        
        dn = ds.index[0]
        print("saving...", name_to_save)
        
        fig = dg.plot_vertical_drift_and_pre(ds)
        
        month_name = dn.strftime("%m")
                
        save_it = os.path.join(
            save_in, month_name, name_to_save 
            )
        save_but_not_show(fig, save_it)
        
        