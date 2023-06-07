import pandas as pd
import numpy as np
import datetime


def find_header(infile: str, 
                header: str = 'yyyy.MM.dd'
                ) -> tuple:
    
    """Function for find the header and the data section"""
    
    with open(infile) as f:
        data = [line.strip() for line in f.readlines()]
    
    count = 0
    for num in range(len(data)):
        if (header) in data[num]:
            break
        else:
            count += 1

    data_ = data[count + 2:]
    
    header_ = data[1].split()
    
    return (header_, data_)


def time_to_float(intime) -> float:
    """
    Function for to convert time into float number
    Parameters
    ---------
        intime: str (like "22:10:00") or datetime.time or datetime.datetime
    >>> intime = datetime.datetime(2013, 1, 1, 22, 10, 0)
    >>> time_to_float(intime)
    ... 22.167
    """
    try:
        if (isinstance(intime, datetime.datetime) or 
            isinstance(intime, datetime.time)):
            
            time_list = [intime.hour, 
                         intime.minute, 
                         intime.second]
            
        elif ":" in intime:
            time_list = [int(num) for num 
                         in str(intime).split(":")]
    except:
        raise TypeError("The input parameter" + 
                        "must be datetime.datime or clock format")
        
    return round(time_list[0] + 
                 (time_list[1] / 60) + 
                 (time_list[2] / 3600), 3)


def structure_the_data(data: list) -> np.array:
    
    """
    Function for organize the data (get from find_header function)
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
    
      
def fixed_frequencies(infile):
    
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
    
    df["time"] = df["time"].apply(lambda x: time_to_float(x))
    
    for col in df.columns[3:]:
        
        name = int(float(col))
        
        df.rename(columns = {col: name}, 
                  inplace = True)
        
        df[name] = df[name].apply(
            pd.to_numeric, errors = 'coerce'
            )
        
    df.drop(columns = {"date", "doy"}, 
            inplace = True) 
    
    return df
        
# infile = 'database/Digisonde/raw'

# fixed_frequencies(infile).to_csv('SAA0K_20130216_freq.txt')