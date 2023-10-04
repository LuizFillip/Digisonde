import digisonde as dg
import numpy as np
import pandas as pd
import base as b


def vertical_drift(
        df: pd.DataFrame, 
        set_cols = None, 
        smooth = True
        ) -> pd.DataFrame:
    
    """
    Compute the vertical drift with 
    (dh`F/dt) from ionosonde fixed frequency 
    (in meters per second)
    """
    
    ds = df.copy()
    
    if set_cols is None:
        columns = ds.columns
    else:
        columns = set_cols
        
    for col in columns:
        
        if col != "time":
            
            if smooth:
                ds[col] = b.smooth2(ds[col], 5)
        
            ds[col] = (ds[col].diff() / 
                       ds["time"].diff()) / 3.6

    ds["vz"] = np.mean(
        ds[columns[1:]], 
        axis = 1
        )
    
    return ds


def get_maximum_row(ts, dn, N = 5):
    
    ts = ts[['vz', 'evz']]
    
    ts['max'] = ts['vz'].max()
    ts['filt'] = b.running(ts['vz'], N)
    
    ds = dg.sel_between_terminators(ts, dn)
    
    if len(ds) == 0:
        ds = ts.copy()
        
    ds = ds.sort_values(
        'vz',  
        ascending = False
        ).round(3)
    

    return ds.iloc[0, :].to_frame().T 

def PRE_from_SAO(infile):
    

    vz = vertical_drift(
         dg.fixed_frequencies(infile)
         )

    vz['evz'] = vz.std(axis = 1)
    
    out = []
    for dn in np.unique(vz.index.date):
        
        ts = vz.loc[vz.index.date == dn]
        
        out.append(
            get_maximum_row(ts, dn, N = 5)
            )
    
    return pd.concat(out)



pd.set_option('mode.chained_assignment', None)


def join_drift_sao(ds, df):
    
    df1 = pd.concat([ds, df]).sort_index()
    
    df1['time'] = df1.index.time
    
    df1.index = pd.to_datetime(df1.index.date)
    
    df1['filt'].fillna(df1['vz'], inplace = True)
    
    return df1.sort_index()


# # def main():
# year = 2021


# infile = f"D:\\drift\\{year}.txt"
# df = b.load(infile)

# infile = f'database/iono/{year}'

# ds = PRE_from_SAO(infile)

# ds = ds.interpolate()

# ds1 = join_drift_sao(ds, df)
# # 
# ds1['filt'].plot()



# ds1