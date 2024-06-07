import base as b
import pandas as pd
import digisonde as dg 

PATH_IONO = 'digisonde/data/chars/midnight/'

def pivot(df, parameter = 'hF2'):
    df['time'] = b.time2float(df.index, sum_from = 18)
    
    df['day'] = df.index.day 
    df[parameter] = b.smooth2(df[parameter], 3)
    
    return pd.pivot_table(
        df,
        values = parameter,
        columns = 'day',
        index = 'time'
        ) 

def get_mean(ds, parameter):
    data = {
        parameter: ds.mean(axis = 1), 
        'd' + str(parameter) : ds.std(axis = 1)
        }
    return pd.DataFrame(data, index = ds.index)


def IonoAverage(infile, parameter = 'hF2'):
    
    df = dg.chars(PATH_IONO + infile)
    
    ds = pivot(df, parameter)
    
    return  get_mean(ds, parameter)
    
    
def get_mean_in_col(file, cols, parameter = 'vz'):
    df = dg.IonoChar(file, cols).drift()
    df = df.between_time('20:00', '08:00')
     
    ds = pivot(df, parameter).interpolate()
    
    return get_mean(ds, parameter)

def DriftAverage(file, cols):
    
    out = []
    
    for col in cols:
     
        out.append(get_mean_in_col(file, cols, parameter = col))
        
    ds = pd.concat(out, axis = 1)
    
    st_c = [f'd{c}' for c in cols ]
    data = {
        'vz': ds[cols].mean(axis = 1), 
        'dvz': ds[st_c].mean(axis = 1)
        }
    
    return pd.DataFrame(data, index = ds.index)





def main(file):
    
    import datetime as dt 
    
    
    df = dg.IonoChar(file).drift()
    
    days = sorted(list(set(df.index.date)))
    
    dates = [dt.datetime(2015, 12, 3), 
     dt.date(2015, 12, 4), 
     dt.date(2015, 12, 18),
     dt.date(2015, 12, 28), 
     dt.date(2015, 12, 29), 
    ]
    df = df.loc[df.index.date.isin(dates)]
    
    
        # def main():
    file = 'SAA0K_20151202(336).TXT'
    
    
    cols = list(range(4, 8, 1))
    
    ds = DriftAverage(file, cols)

    ds['vz'].plot()


