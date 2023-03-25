import datetime as dt
import os
import numpy as np
import pandas as pd
import math

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
            
def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    return np.convolve(y, box, mode = 'same')


def time2float(time_array, sum24 = False):
    out = []

    for arr in time_array:
        
        hour = (arr.hour + 
                arr.minute / 60)
        if sum24:
            if hour < 20:
                hour += 24
        
        out.append(hour)
    return out

class ionosonde_fname(object):

    def __init__(self, filename):
    
        args = filename.split("_")
    
        self.code = args[0]
    
        self.date = args[1][:8]
    
        self.time = args[1][13:-4]
        
        str_datetime = self.date + self.time
    
        self.datetime = dt.datetime.strptime(str_datetime, 
                                             "%Y%m%d%H%M%S")
        
        
def split_time(time):
    frac, whole = math.modf(float(time))
    return int(whole), round(frac * 60)

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
