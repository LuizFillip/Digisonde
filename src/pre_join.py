import base as b
import pandas as pd

def join_data(df, year):
        
    infile = 'digisonde/data/PRE/saa/2014_2015_2.txt'
    df2 = b.load(infile)

    df2 = df2[df2.index.year == year]
    
    df.index = pd.to_datetime(df.index)
    ds = pd.concat([df2, df])
    
    return ds.drop_duplicates()


def run_years():
    
    out = []
    
    for year in np.arange(2013, 2023):
        
        infile = 'digisonde/data/drift/data/'
        
        fname = f'{year}_drift.txt'
        
        df = get_pre_in_year(infile + fname).dropna()
        
        if (year == 2014 ) or (year == 2015):
            
            ds = join_data(df, year).copy()
        else:
            ds = df.copy()

        out.append(ds)
        
    return pd.concat(out)
        

def join_sao_and_drift(
        year = 2014, 
        col = 'vp'
        ):
    
    drift_file = f'digisonde/data/drift/PRE/saa/{year}.txt'
    sao_file = 'digisonde/data/PRE/saa/2014_2015_2.txt'
    
    df = b.load(drift_file)[col]
    df1 = b.load(sao_file)[col]
    
    df1 = df1.loc[df1.index.year == year]
    
    ds = pd.concat([df1, df]).sort_index()
    
    return ds.groupby(ds.index).first().to_frame(col)




def replacing_values():
    
    infile = 'digisonde/data/drift/data/2022_drift.txt'
    
    df = b.load(infile)
    
    ds = b.load('pre_all_years.txt').replace(0, np.nan)
        
    ds = ds['vp'].to_frame('vp').dropna()
    
    df = dg.concat_all_pre_values().dropna()
    
    df2 = pd.concat([df, ds])
     
    df2 = df2.drop_duplicates()
    
    
    df2.to_csv('pre_all_years_2.txt')
    