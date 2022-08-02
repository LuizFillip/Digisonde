# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 18:06:16 2022

@author: Luiz
"""
import os
import pandas as pd
import config
infile = "Database/QF/"

_, _, files = next(os.walk(infile))



filename = files[0]

out = []

for filename in files:
    df = pd.read_csv(infile + filename, 
                     header = 5, 
                     delim_whitespace=(True), 
                     index_col=(False),
                     names = ["date","doy", "time", "qf"])
    
    df.index = pd.to_datetime(df["date"] +" " + df["time"])

    out.append(df["qf"])
    
dd = pd.concat(out)

dd.plot()