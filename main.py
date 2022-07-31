# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 17:34:01 2022

@author: Luiz
"""

from ionosonde import *
from prereversalEnhancement import *
from plotVerticaldrift import *
from tqdm import tqdm


def result_per_day(infile, filename):

    outside_day = []
    
    for day in range(1, 32, 1):
        
        df = select_day(infile, filename, day)
        
        if df.empty:
            print(f"No data for the {day}")
            pass
        else:
            try:
                print(f"{day} was collected!")
                # Save without show the plots
                plotVerticaldrift(infile, filename, day, save = True)
                
                # Extract PRE values 
                outside_day.append(PRE(infile, filename, day))
                
            except:
                print(f"{day} not was collected!")
                pass
            
    return pd.concat(outside_day)

def result_per_month(infile, year = 2014):
    
    _, _, files = next(os.walk(infile))
    
    global status
    
    outside_month = []
    
    total = len(files)
    with alive_bar(total) as bar:
        for filename in files:
            if str(year) in filename:
                try:
                    # Get results by day
                    outside_month.append(result_per_day(infile, filename))
                    status = filename.replace("FZA0M_", "").replace(".txt", "")
                    print(f"Month {status} passed!")
                except:
                    print(f"Month{status} not passed!")
                    pass
                
        print(f"{year} finished")
        
        
    if len(outside_month) > 0:
        result =  pd.concat(outside_month)
    else:
        pass
    
    return result


def save(infile, year):
    
    df = result_per_month(infile, year = year)
    
    if "SL" in infile:
        site = "Saoluis"
    else:
        site = "Fortaleza"
    
    return df.to_csv(f"Results/{site}/PRE/{year}.txt", 
                     sep = " ", index = True)



from alive_progress import alive_bar
from alive_progress.styles import showtime
import time

def main()

    for city in ["FZ"]:
        for year in [2014, 2015]:
            infile = f"Database/{city}_2014-2015_Processado/"
            #print(city, year, infile)
            
            save(infile, year)
