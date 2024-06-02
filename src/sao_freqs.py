import pandas as pd
import numpy as np
import base as b

def find_header(
        infile: str, 
        header: str = 'yyyy.MM.dd'
        ) -> tuple:
    
    """Function for find the header
    and the data section"""
    
    with open(infile) as f:
        data = [line.strip() for line in f.readlines()]
    
    count = 0
    for num in range(len(data)):
        if (header) in data[num]:
            break
        else:
            count += 1
            
    return data[1].split(), data[count + 2:]



def structure_the_data(data: list) -> np.array:
    
    """
    Function for organize the data 
    (get from find_header function)
    in array format
    """
    out_second = []
    for first in range(len(data)):
        
        out_first = []
        out_second.append(out_first)
        
        for second in data[first].split():
            
            rules = [second != "/", 
                     second != '//',
                     second != '---']
            
            if all(rules):
                out_first.append(second)
            else:
                out_first.append(np.nan)
    
    return np.array(out_second)
    
      
def freq_fixed(infile, snum = 2):
    
    """
    Get pandas dataframe from the data (already organized), 
    with datetime index, frequencies values in float format
    """

    header, data = find_header(infile)
    
    df = pd.DataFrame(structure_the_data(data), 
                      columns = header)
    
    df.rename(columns = {
        "yyyy.MM.dd": "date", 
        "HH:mm:ss": "time", 
        "(DDD)": "doy"}, 
        inplace = True
        )
    
    df.index = pd.to_datetime(df["date"] + " " + df["time"])
    
    for col in df.columns[3:]:
        
        name = int(float(col))
        
        df.rename(columns = {col: name}, inplace = True)
        
        df[name] = df[name].apply(pd.to_numeric, errors = 'coerce')
        
    df.drop(columns = {"date", "doy"}, inplace = True) 
    
    # for col in df.columns:
    #     df[col] = b.smooth2(df[col], snum)
    
    return df

