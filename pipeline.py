# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 11:44:53 2022

@author: Luiz
"""

#from ionosonde import *
import pandas as pd
import numpy as np



def EPBsEvents():
    
    infile = "C:\\Users\\Luiz\\OneDrive\\Documentos\\Scripts\\EPB_Probability_2014.xlsx"
    
    df = pd.read_excel(infile, sheet_name= "EPBsEvents", header = 1)
    
    df.index = pd.to_datetime(df["date"], format='%Y%m%d')
    
    df[df.columns[2:]] = df[df.columns[2:]].apply(pd.to_numeric, 
                                                  errors='coerce')
    
    df.drop(columns = ["date", "(deg) South"], inplace = True)
    
    return df


city = "Fortaleza"
infile = f"Results/{city}/PRE/"
filename = "2014.txt"

def sel_parameter(infile, filename, factor = "peak"):
    
    df = pd.read_csv(infile + filename, 
                     delim_whitespace=(True), 
                     index_col = [0, 1])
    
    df = df.loc[(df.index.get_level_values('Values') ==  factor), :]
    
    df.index = pd.to_datetime(df.index.get_level_values(0))
    return df

def save(infile, filename, factor = "peak"):
    
    df = pd.concat([sel_parameter(infile, filename, factor = factor), 
                    EPBsEvents()], axis = 1)
    
    return df.to_csv(f"EPBsEventsAndPRE_{city}2014.txt", 
              index = True, sep = " ")

