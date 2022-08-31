 # -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 19:47:03 2022

@author: Luiz
"""

import pandas as pd
import numpy as np
import os
import datetime
from unidecode import unidecode
pd.options.mode.chained_assignment = None

def doy_str_format(date: int) ->str:
    
    if isinstance(date, datetime.datetime):
        doy = date.timetuple().tm_yday
    else:
        doy = date
    
    if doy < 10:
        FigureName = f"00{doy}"
        
    elif doy >= 10 and doy < 100:
        FigureName = f"0{doy}"

    else:
        FigureName = f"{doy}"
        
    return FigureName

def find_header(infile:str, 
                filename: str, 
                header: str = 'yyyy.MM.dd') -> tuple:
    
    """Function for find the header and the data body"""
    
    with open(infile + filename) as f:
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
            
            time_list = [intime.hour, intime.minute, intime.second]
            
            
        elif ":" in intime:
            time_list = [int(num) for num in str(intime).split(":")]
    except:
        raise TypeError("The input parameter must be datetime.datime or clock format")
        
    return round(time_list[0] + 
                 (time_list[1] / 60) + 
                 (time_list[2] / 3600), 3)



def structure_the_data(data: list) -> np.array:
    
    """
    Function for organize the data (get from find_header function)
    in array format
    """
    
    
    outside_second = []
    for first in range(len(data)):
        
        outside_first = []
        outside_second.append(outside_first)
        
        for second in data[first].split():
            
            rules = [second != "/", 
                     second != '//',
                     second != '---']
            
            if all(rules):
                outside_first.append(second)
            else:
                outside_first.append(np.nan)
    
    return np.array(outside_second)
    

def select_day(infile: str, 
               filename: str, 
               day: int = 1,
               columns: list = ["time", 6, 7, 8], 
               begin_time: str = '18:00:00', 
               end_time: str = '23:50:00') -> pd.DataFrame:
    
    """
    Get pandas dataframe from the data (already organized), 
    with datetime index, frequencies values in float format
    """
    
    header, data = find_header(infile, filename)
    
    df = pd.DataFrame(structure_the_data(data), 
                      columns = header)
    
    df.rename(columns = {"yyyy.MM.dd": "date", 
                         "HH:mm:ss": "time", 
                         "(DDD)": "doy"}, inplace = True)
    
    df.index = pd.to_datetime(df["date"] + " " +
                              df["time"])
    
    df["time"] = df["time"].apply(lambda x: time_to_float(x))
    
    for col in df.columns[3:]:
        
        name = int(float(col))
        
        df.rename(columns = {col: name}, 
                  inplace = True)
        
        df[name] = df[name].apply(pd.to_numeric, 
                                          errors='coerce')
    
    
    df = df.loc[df.index.day == day, columns]
    
    if begin_time:
        df = df.between_time(begin_time, end_time)
    
    
    return df
    


def drift(df: pd.DataFrame) -> pd.DataFrame:
    
    """Compute the vertical drift with (dh`F/dt) in meters per second"""
    
    data = df.copy()
        
    for col in data.columns:
        
        if col != "time":
        
            data[col] = (data[col].diff() / data["time"].diff()) / 3.6
    
    return data



def sel_parameter(infile, filename, factor = "peak"):
    
    df = pd.read_csv(infile + filename, 
                     delim_whitespace=(True), 
                     index_col = [0, 1])
    
    df = df.loc[(df.index.get_level_values('Values') ==  factor), :]
    
    df.index = pd.to_datetime(df.index.get_level_values(0))
    return df

