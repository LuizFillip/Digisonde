import os
import datetime

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


        
def infos_from_filename(filename):
    
    """Getting site informations by filename"""
    
    dat = infos_iono["Brazil"]
    keys = dat.keys()

    for key in keys:
        if key in filename:
            name = dat[key]["name"]
            lat = dat[key]["lat"]
            lon = dat[key]["lon"]
            return name, lat, lon
        else:
            raise ValueError(f"Could not find the coordinates of {filename}")
            
    

def main():
    infile = "database/FZ_2014-2015_Processado/"
    
    _, _, files = next(os.walk(infile))
    
    filename = files[0]
    
    name, lat, lon = infos_from_filename(filename)
    
    print(lat)

