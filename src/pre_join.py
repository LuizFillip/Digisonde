import base as b
import pandas as pd

def join_data(df, year):
        
    infile = 'digisonde/data/PRE/saa/2014_2015_2.txt'
    df2 = b.load(infile)

    df2 = df2[df2.index.year == year]
    
    df.index = pd.to_datetime(df.index)
    ds = pd.concat([df2, df])
    
    return ds.drop_duplicates()


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


infile = 'digisonde/data/drift/data/saa/2023_drift.txt'


df = b.load(infile)
df = df.replace(0, float('nan'))


df[['vz']].dropna()