# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 16:49:11 2022

@author: Luiz
"""


import os

from astral.sun import sun
import astral 
import datetime
import requests



def get_coords(city: str, 
               country: str = "Brazil") -> tuple:
    import requests

    
    """
    Function for get latitude and longitude
    from name of city and country. Use 'Request' library
    for scrapy these informations
    -----
    Example
    -------
    get_coords(city = 'Campina Grande', 
               country = 'Brazil')
    >>> (-7.22, -35.88)
    """

    url_site = "https://nominatim.openstreetmap.org/?" 
    
    addressdetails = f"addressdetails=1&q={city}+{country}&format=json&limit=1"
    
    response = requests.get(url_site + addressdetails).json()
    
    lat = float(response[0]["lat"])
    lon = float(response[0]["lon"])
    return (round(lat, 3), round(lon, 3))


class site(object):
    
    def __init__(self, filename: str, 
                 country: str = "Brazil"):
        
        self.filename = filename
        self.country = country
        
        acronym = self.filename[:3]
        
        if acronym == "SAA":
            self.latitude = -2.53
            self.longitude = -44.296
            self.name = "São Luis"
            
        elif acronym == "FZA":
            self.latitude = -3.73
            self.longitude = -38.522
            self.name = "Fortaleza"
            
        else:
            try:
                coords = get_coords(city = self.filename, 
                                    country = self.country)
                
                self.latitude, self.longitude = coords
                self.name = self.filename
            except:
                raise ValueError(f"Could not find the coordinates of {self.filename}")

def time_to_float(intime):
    
    elem = [intime.hour, intime.minute]
    
    time = [int(num) for num in elem]

    return round(time[0] + (time[1] / 60), 2)
            
class terminators(object):
    
    
    def __init__(self, 
                 filename, 
                 twilightAngle = 18, 
                 date = datetime.date(2014, 1, 1)):
        
        
        self.filename = filename
        self.twilightAngle = twilightAngle
        self.date = date
    
    
    
        info = site(self.filename)
        
        
        observer = astral.Observer(latitude = info.latitude, 
                                   longitude = info.longitude)
        
        
        self.infos = sun(observer, 
                         self.date, 
                         dawn_dusk_depression = self.twilightAngle)
        
        
    
    @property
    def dusk(self):
        
        return time_to_float(self.infos["dusk"])
    
    @property
    def sunset(self):
        
        return time_to_float(self.infos["sunset"])

def main():
    infile = "Database/SL_2014-2015_Processado/"
    
    _, _, files = next(os.walk(infile))
    
    filename = files[0]
        
    print(terminators(filename).sunset)
    
main()