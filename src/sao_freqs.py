import pandas as pd
import numpy as np
import datetime as dt
import base as b

def find_header(
        infile: str, 
        header: str = 'yyyy.MM.dd'
        ) -> tuple:
    
    """Function for find the header
    and the data section"""
    
    with open(infile) as f:
        data = [line.strip() for line 
                in f.readlines()]
    
    count = 0
    for num in range(len(data)):
        if (header) in data[num]:
            break
        else:
            count += 1
            
    return data[1].split(), data[count + 2:]


def time_to_float(dn) -> float:
    """
    Function for to convert time into float number
    Parameters
    ---------
        dn: str (like "22:10:00") or datetime.time 
        or datetime.datetime
    >>> dn = datetime.datetime(2013, 1, 1, 22, 10, 0)
    >>> time_to_float(dn)
    ... 22.167
    """
    try:
        if (isinstance(dn, dt.datetime) or 
            isinstance(dn, dt.time)):
            
            time_list = [dn.hour, 
                         dn.minute, 
                         dn.second]
            
        elif ":" in dn:
            time_list = [int(num) for num 
                         in str(dn).split(":")]
    except:
        raise TypeError("The input parameter" + 
                        "must be datetime or clock format")
        
    return round(time_list[0] + 
                 (time_list[1] / 60) + 
                 (time_list[2] / 3600), 3)


def structure_the_data(data: list) -> np.array:
    
    """
    Function for organize the data 
    (get from find_header function)
    in array format
    """
    out_second = []
    for first in range(len(data)):
        
        out_first = []
        out_second.append(out_first)
        
        for second in data[first].split():
            
            rules = [second != "/", 
                     second != '//',
                     second != '---']
            
            if all(rules):
                out_first.append(second)
            else:
                out_first.append(np.nan)
    
    return np.array(out_second)
    
      
def freq_fixed(infile, snum = 2):
    
    """
    Get pandas dataframe from the data (already organized), 
    with datetime index, frequencies values in float format
    """

    header, data = find_header(infile)
    
    df = pd.DataFrame(structure_the_data(data), 
                      columns = header)
    
    df.rename(columns = {
        "yyyy.MM.dd": "date", 
        "HH:mm:ss": "time", 
        "(DDD)": "doy"}, 
        inplace = True
        )
    
    df.index = pd.to_datetime(
        df["date"] + " " + df["time"]
        )
    
    df["time"] = df["time"].apply(
        lambda x: time_to_float(x))
    
    for col in df.columns[3:]:
        
        name = int(float(col))
        
        df.rename(columns = {col: name}, 
                  inplace = True)
        
        df[name] = df[name].apply(
            pd.to_numeric, 
            errors = 'coerce'
            )
        
    df.drop(columns = {"date", "doy"}, 
            inplace = True) 
    
    for col in df.columns:
        if col != 'time':
            df[col] = b.smooth2(df[col], snum)
    
    return df
        

