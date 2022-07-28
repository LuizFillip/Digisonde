# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 17:34:01 2022

@author: Luiz
"""

from ionosonde import *
from prereversalEnhancement import *
from plotVerticaldrift import *


def result_per_day(infile, filename):
    
    iono = ionosonde(infile, filename)

    outside_day = []
    
    for day in range(1, 32, 1):
        
        df = vertical_drift(iono.select_day(day))
        
        if df.empty:
            print(f"No data for the {day}")
            pass
        else:
            try:
                #get PRE values
                pre_table = PRE(df).table
                
                # Save without show the plots
                #plot(iono, day, save = True)
                
                # Extract out from the loop
                outside_day.append(pre_table)
                print(f"{day} was collected!")
            except:
                print(f"{day} not was collected!")
                pass
            
            
        
        
    return pd.concat(outside_day)

def result_per_month(infile, year = "2014"):
    
    _, _, files = next(os.walk(infile))
    
    outside_month = []
    
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
                
        
        
    return pd.concat(outside_month)

infile = "Database/SL_2014-2015_Processado/"
site = "SaoLuis"
year = 2015
result_by_month(infile, year = year).to_csv(f"{site}{year}.txt", 
                                           sep = " ", index = True)
