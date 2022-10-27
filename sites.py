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


def coords_from_filename(filename):
    
    dat = infos_iono["Brazil"]
    keys = dat.keys()

    for key in keys:
        if key in filename:
            name = dat[key]["name"]
            lat = dat[key]["lat"]
            lon = dat[key]["lon"]
            
        else:
            raise ValueError(f"Could not find the coordinates of {filename}")
            
    
    return name, lat, lon


infile = "Database/FZ_2014-2015_Processado/"

_, _, files = next(os.walk(infile))

filename = files[0]

name, lat, lon = coords_from_filename(filename)

print(lat)

