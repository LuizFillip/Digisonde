from astral.sun import sun
import astral 
import datetime
from sites import infos_from_filename


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
                 (time_list[2] / 3600), 4)

class terminators(object):
    
    
    def __init__(self, 
                 filename, 
                 twilightAngle = 18, 
                 date = datetime.date(2014, 1, 1)):
        
        
        self.filename = filename
        self.twilightAngle = twilightAngle
        self.date = date
    
        # Get informatios about longitude and latitude
        name, lat, lon = infos_from_filename(self.filename)
        
        # Astral library
        observer = astral.Observer(latitude = lat, 
                                   longitude = lon)
        
        # 
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