import datetime as dt
import os
import numpy as np
import pandas as pd
import math
from utils import split_time

embrace_infos = {
                "FZA0M": {"name": "Fortaleza", 
                          "lat":  -3.73, 
                          "lon": -38.522},
                
                "SAA0K": {"name": "Sao luis", 
                          "lat":  -2.53,
                          "lon": -44.296}, 
                
                "BLJ03": {"name": "Belem", 
                          "lat": -1.4563, 
                          "lon": -48.5013}, 
                
                "BVJ03": {"name": "Boa Vista", 
                          "lat":  2.8701, 
                          "lon": -60.7109},
                
                "CGK21": {"name": "Campo Grande", 
                          "lat":  -20.4649, 
                          "lon": -54.6218},
                
                "CAJ2M": {"name": "Cachoeira Paulista", 
                          "lat": -22.7038, 
                          "lon": -45.0093},
                
                "SMK29": {"name": "Santa Maria", 
                          "lat": -29.6897, 
                          "lon": -53.8043},
                }
        
def get_infos(filename):
    
    """Getting EMBRACE sites informations by filename"""
    
    keys = embrace_infos.keys()
    f = filename.split("_")
    for key in keys:
        if (key == f[0]):
            name = embrace_infos[key]["name"]
            lat = embrace_infos[key]["lat"]
            lon = embrace_infos[key]["lon"]
            return name, lat, lon
            


def ionosonde_fname(filename):

    args = filename.split("_")

    str_datetime = args[1][:8] + args[1][13:-4]

    return dt.datetime.strptime(
        str_datetime, 
        "%Y%m%d%H%M%S")
        
        

def get_datetime_pre(dn):
    infile ="database/Digisonde/vzp/FZ_PRE_2014_2015.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
   
    time_sel = df.loc[df.index == dn, "time"]
    
    hour, minute = split_time(time_sel.item())
    
    return dt.datetime(
        dn.year, dn.month, dn.day, 
                hour, minute)


       
def main():
    infile = "database/process/SL_2014-2015/"
    
    _, _, files = next(os.walk(infile))
    
    filename = files[0]
    
    name, lat, lon = get_infos(filename)
    

    print(name, lat, lon)
