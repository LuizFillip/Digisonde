# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 10:55:41 2023

@author: Luiz
"""

import pandas as pd
import datetime as dt
from utils import time2float
import digisonde as dg


def quiet_days_mean():

    infile = "database/Drift/SSA/PRO_2013.txt"
    
    dig = dg.load_drift(infile)
    
    times = pd.date_range('2013-03-06', '2013-03-13', freq = '1D')
    
    out = []
    for i in range(len(times) - 1):
        df = dig.loc[(dig.index >= times[i]) &
                (dig.index <= times[i + 1] - dt.timedelta(minutes = 30))]['vz']
        
        df.index = time2float(df.index, sum24_from = None)
        
        out.append(df.to_frame(times[i]))
        
    df = pd.concat(out, axis = 1)

# df.mean(axis = 1).to_csv("mean.txt")




