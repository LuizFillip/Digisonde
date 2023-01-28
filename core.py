import pandas as pd
import numpy as np
import datetime
pd.options.mode.chained_assignment = None



def find_header(infile: str, 
                header: str = 'yyyy.MM.dd'
                ) -> tuple:
    
    """Function for find the header and the data section"""
    
    with open(infile) as f:
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
            time_list = [int(num) for num 
                         in str(intime).split(":")]
    except:
        raise TypeError("The input parameter" + 
                        "must be datetime.datime or clock format")
        
    return round(time_list[0] + 
                 (time_list[1] / 60) + 
                 (time_list[2] / 3600), 3)



def structure_the_data(data: list) -> np.array:
    
    """
    Function for organize the data (get from find_header function)
    in array format
    """
    
    
    outside_second = []
    for first in range(len(data)):
        
        outside_first = []
        outside_second.append(outside_first)
        
        for second in data[first].split():
            
            rules = [second != "/", 
                     second != '//',
                     second != '---']
            
            if all(rules):
                outside_first.append(second)
            else:
                outside_first.append(np.nan)
    
    return np.array(outside_second)
    

class iono_frame(object):
    
    """
    Get pandas dataframe from the data (already organized), 
    with datetime index, frequencies values in float format
    """
    
    def __init__(
            self, 
            infile: str,  
            day: int = 1,
            columns: list = ["time", 6, 7, 8], 
            ) -> pd.DataFrame:
    
        self.columns = columns
    
        header, data = find_header(infile)
        
        df = pd.DataFrame(structure_the_data(data), 
                          columns = header)
        
        df.rename(columns = {"yyyy.MM.dd": "date", 
                             "HH:mm:ss": "time", 
                             "(DDD)": "doy"}, 
                  inplace = True)
        
        df.index = pd.to_datetime(df["date"] + 
                                  " " +
                                  df["time"])
        
        df["time"] = df["time"].apply(lambda x: time_to_float(x))
        
        for col in df.columns[3:]:
            
            name = int(float(col))
            
            df.rename(columns = {col: name}, 
                      inplace = True)
            
            df[name] = df[name].apply(pd.to_numeric, 
                                      errors='coerce')
            
        df.drop(columns = {"date", "doy"}, 
                inplace = True) 
        
        self.df = df
        
        self.days = np.unique(df.index.day)
        
        
    def sel_day(self, day = 1):
        """Select one single day"""
        return self.df.loc[self.df.index.day == day, self.columns]
    
    def sel_day_in(self, 
                   day = 1, 
                   begin_time: str = '18:00:00', 
                   end_time: str = '23:50:00'):
        """Select time range in day"""
        return self.sel_day(day).between_time(begin_time, end_time)

    
    
def sel_parameter(infile, factor = "peak"):
    
    df = pd.read_csv(infile, 
                     delim_whitespace=(True), 
                     index_col = [0, 1])
    
    df = df.loc[(df.index.get_level_values('Values') ==  factor), :]
    
    df.index = pd.to_datetime(df.index.get_level_values(0))
    return df


def main():

    infile = "database/process/SL_2014-2015/SAA0K_201401.txt"
    
    df = iono_frame(infile).sel_day()
    
    print(df)


