import digisonde as dg 
import base as b 
import pandas as pd
import aeronomy as io

infile = 'digisonde/data/SAO/profiles/'

def storm_profiles(site = 'FZA0M'):
    
    path_profiles = 'digisonde/data/SAO/profiles/'
    
    files = [
        f'{site}_20151219(353).TXT', 
        f'{site}_20151220(354).TXT', 
        f'{site}_20151221(355).TXT', 
        f'{site}_20151222(356).TXT'
        ]
    
    out = []
    
    for fn in files:
        infile = path_profiles + fn 
        
        out.append(dg.Profilegram(infile))
        
    df = pd.concat(out)
    
    df["ne"] = (1.24e4 * df["freq"]**2) * 1e6
    df["L"] = io.scale_gradient(df["ne"], df["alt"])
    
    return df 



def quiettime_gradient_scale(
        site = 'SAA0K', 
        alt = 250, parameter = 'L'
        ):
    
    
    files = [
        f'{site}_20151213(347).TXT',
        f'{site}_20151216(350).TXT', 
        f'{site}_20151218(352).TXT', 
        f'{site}_20151229(363).TXT'
        ]


    out = []
    
    
    for fn in files:
        
        df = dg.Profilegram(infile + fn)
        
        df.index = pd.to_datetime(df.index)
        
        df["ne"] = (1.24e4 * df["freq"]**2) * 1e6
        
        df["L"] = io.scale_gradient(df["ne"], df["alt"])
        
        df = df.loc[df['alt'] == alt, [parameter]]
        
        df.index = b.time2float(
            df.index, 
            sum_from = None
            )
        
        df = df.loc[~df.index.duplicated()]
        
        out.append(df.iloc[:-1])
        
    ds = pd.concat(out, axis = 1).sort_index()
    
    df = pd.DataFrame()
    df['L'] = ds.mean(axis = 1)
    df['dL'] = ds.std(axis = 1)
    return df
    
   
    
    
