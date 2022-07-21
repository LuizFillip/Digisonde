# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 19:47:03 2022

@author: Luiz
"""

import pandas as pd
import numpy as np
import os


class ionosonde:
    
    def __init__(self, infile, filename):
        self.infile = infile
        self.filename = filename
        
        with open(self.infile + self.filename) as f:
            data = [line.strip() for line in f.readlines()]
        
        count = 0
        for num in range(len(data)):
            if ('yyyy.MM.dd') in data[num]:
                break
            else:
                count += 1
        
        data = data[count:]
        
        
        reader = data[0].split()
        
        listA = [str(float(num)) for num in range(3, 9)] 
        res = [ele for ele in listA if(ele in reader)]
        
        raw_data = []
        
        
        if (res == listA):
            for num in range(2, len(data)):
                raw = []
                raw_data.append(raw)
                for element in data[num].split():
                    if element != '---':
                        raw.append(element)
                    else:
                        raw.append(np.nan)
            
            columns_to_drop = ['yyyy.MM.dd', '(DDD)', 'HH:mm:ss']
        else:
            for num in range(2, len(data)):
        
                raw = []
                raw_data.append(raw)
                
                for element in data[num].split():
                    if (element != "/") and (element != '//'):
                        raw.append(element)
                        
            raw_data = raw_data[:-8]
            
            columns_to_drop = ['yyyy.MM.dd', '(DDD)', 'HH:mm:ss', 'C-score']
            
        self.df = pd.DataFrame(raw_data, columns = reader)
     
        self.df.index = pd.to_datetime(self.df["yyyy.MM.dd"] + " " + self.df["HH:mm:ss"])
     
        self.df.drop(columns = columns_to_drop, inplace = True)
     
        self.df[self.df.columns] = self.df[self.df.columns].apply(pd.to_numeric, errors='coerce')
    
    @property    
    def data(self):
        return self.df.between_time('18:00:00', '22:50:00')
    
    def vertical_drift(self, columns = ['3.0', '4.0', '5.0', 
                                        '6.0', '7.0', '8.0']):
        
        values = self.df.index.hour.values
        minute = self.df.index.minute.values / 60
        second = self.df.index.second.values / 3600
        
        hour = np.where(values >= 9, values, values + 24)
        time = np.array(hour + second + minute)
        
        self.df["time"] = time
        for col in self.df.columns[:-1]:
            
            self.df[col] = (self.df[col].diff() / self.df["time"].diff()) / 3.6
        
        return self.df[columns].between_time('18:00:00', '23:00:00')
    
    
       

# = 

#(result)
   
        
