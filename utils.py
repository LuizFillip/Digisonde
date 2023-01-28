import datetime as dt
import os

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
    infile = "database/process/SL_2014-2015/"
    
    _, _, files = next(os.walk(infile))
    
    filename = files[0]
    
    name, lat, lon = get_infos(filename)
    

    print(name, lat, lon)
main()