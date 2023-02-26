from astral.sun import sun
import astral 
import datetime
from Digisonde.utils import get_infos
from Digisonde.core import time_to_float



class terminators(object):
    
    
    def __init__(self, 
                 filename, 
                 twilightAngle = 18, 
                 date = datetime.date(2014, 1, 1)):
        
        
        self.filename = filename
        self.twilightAngle = twilightAngle
        self.date = date
    
        # Get informatios about longitude and latitude
        name, lat, lon = get_infos(self.filename)
        
        # Astral library
        observer = astral.Observer(latitude = lat, 
                                   longitude = lon)
        
         
        self.sun_phase = sun(observer, self.date, 
                         dawn_dusk_depression = self.twilightAngle)
        
    @property
    def dusk(self):
        """
        The time in the evening when the sun is a specific 
        number of degrees below the horizon.
        """
        return time_to_float(self.sun_phase["dusk"])
    
    @property
    def sunset(self):
        """
        The time in the evening when the sun is about to disappear 
        below the horizon (asuming a location with no obscuring features.)
        """
        return time_to_float(self.sun_phase["sunset"])