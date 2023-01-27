import datetime as dt
import os

infos_iono = {"Brazil": 
              {
                "FZA0M": {"name": "Fortaleza", 
                          "lat":  -3.73, 
                          "lon": -38.522},
                "SAA0K": {"name": "Sao luis", 
                          "lat":  -2.53,
                          "lon": -44.296} , 
                "BLJ03": {"name": "Belem"}  
                }}
        
def EMBRACE_infos(filename):
    
    """Getting EMBRACE sites informations by filename"""
    
    dat = infos_iono["Brazil"]
    keys = dat.keys()

    for key in keys:
        if key in filename:
            name = dat[key]["name"]
            lat = dat[key]["lat"]
            lon = dat[key]["lon"]
            return name, lat, lon
        else:
            raise ValueError("Could not find the" +
                             f"coordinates of {filename}")
            

class ionosonde_fname(object):

    def __init__(self, filename):
    
        args = filename.split("_")
    
        self.code = args[0]
    
        self.date = args[1][:8]
    
        self.time = args[1][13:-4]
        
        str_datetime = self.date + self.time
    
        self.datetime = dt.datetime.strptime(str_datetime, 
                                             "%Y%m%d%H%M%S")
        
        
        
def main():
    infile = "database/FZ_2014-2015_Processado/"
    
    _, _, files = next(os.walk(infile))
    
    filename = files[0]
    
    name, lat, lon = EMBRACE_infos(filename)
    
    print(lat)
