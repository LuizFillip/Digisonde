 # -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 19:47:03 2022

@author: Luiz
"""

import pandas as pd
import numpy as np
import os
import datetime
pd.options.mode.chained_assignment = None


def find_header(infile:str, 
                filename: str, 
                header: str = 'yyyy.MM.dd') -> tuple:
    
    
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




def time_to_float(time: str) -> float:
    
    elem = str(time)
    
    time = [int(num) for num in elem.split(":")[:2]]
    current = round(time[0] + (time[1] / 60), 2)
    
    return current

def structure_the_data(data: list) -> np.array:
    
    
    outside_second = []
    for num in range(len(data)):
        
        outside_first = []
        outside_second.append(outside_first)
        
        for element in data[num].split():
            
            rules = [element != "/", 
                     element != '//',
                     element != '---']
            
            if all(rules):
                outside_first.append(element)
            else:
                outside_first.append(np.nan)
    
    return np.array(outside_second)
    

def select_day(infile: str, 
               filename: str, 
               day: int = 1,
               columns: list = ["time", 6, 7, 8], 
               begin_time: str = '18:00:00', 
               end_time: str = '23:50:00') -> pd.DataFrame:
    
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
    
    data = df.copy()
        
    for col in data.columns:
        
        if col != "time":
        
            data[col] = (data[col].diff() / data["time"].diff()) / 3.6
    
    return data




def main():

    infile = "Database/SL_2014-2015_Processado/"
    
    _, _, files = next(os.walk(infile))
    
    filename = files[0]
    
    df = select_day(infile, filename, 1).interpolate()
    
    dd = drift(df)
    
    
