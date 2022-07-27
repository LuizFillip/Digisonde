# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 17:34:01 2022

@author: Luiz
"""

from ionosonde import *
from prereversalEnhancement import *
#from plotVerticaldrift import *


def result_by_day(infile, filename):
    
    iono = ionosonde(infile, filename)

    result_by_day_ = []
    
    for day in range(1, 32, 1):
        
        df = vertical_drift(iono.select_day(day))
        
        if df.empty:
            print(f"No data for the {day}")
            pass
        else:
            try:
                pre_table = PRE(df).table
                result_by_day_.append(pre_table)
                print(f"{day} was collected!")
            except:
                print(f"{day} not was collected!")
                pass
            
            
        
        
    return pd.concat(result_by_day_)

def result_by_month(infile, year = "2014"):
    
    _, _, files = next(os.walk(infile))
    
    result_by_month_ = []
    
    for filename in files:
        if year in filename:
            try:
                result_by_month_.append(result_by_day(infile, filename))
                status = filename.replace("FZA0M_", "").replace(".txt", "")
                print(f"Month {status} passed!")
            except:
                print(f"Month{status} not passed!")
                pass
                
        
        
    return pd.concat(result_by_month_)

infile = "Database/FZ_2014-2015_Processado/"
#result_by_month(infile).to_csv("Fortaleza2014.2.txt", sep = " ", index = True)
