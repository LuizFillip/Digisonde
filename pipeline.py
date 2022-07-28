# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 11:44:53 2022

@author: Luiz
"""

from ionosonde import *


# =============================================================================
# 
# =============================================================================
def EPBsEvents():
    
    infile = "C:\\Users\\Luiz\\OneDrive\\Documentos\\Scripts\\EPB_Probability_2014.xlsx"
    
    df = pd.read_excel(infile, sheet_name= "EPBsEvents", header = 1)
    
    df.index = pd.to_datetime(df["date"], format='%Y%m%d')
    
    df[df.columns[2:]] = df[df.columns[2:]].apply(pd.to_numeric, 
                                                  errors='coerce')
    
    df.drop(columns = ["date", "(deg) South"], inplace = True)
    
    return df

#print(EPBsSheet())
# =============================================================================
# 
# =============================================================================

#
class select_parameter(object):
    
    def __init__(self, filename):
        self.filename = filename
    

        self.df = pd.read_csv(filename, 
                         delim_whitespace=(True), 
                         index_col = [0, 1])
        
    
    def peak(self, sunset = False):
        self.df = self.df.iloc[(self.df.index.get_level_values('Values') == 
                                "Peak (m/s)"), :]
        
        self.df[self.df.columns] = self.df[self.df.columns].apply(pd.to_numeric, 
                                                                  errors='coerce')
        self.df.index = pd.to_datetime(self.df.index.get_level_values(0))
        
        try:
            if sunset is False:
                self.df.drop(columns = ["sunset"], inplace = True)
        except:
            pass
        return self.df
        
    def time(self, current = True):
        self.df = self.df.iloc[(self.df.index.get_level_values('Values') == 'Time (UT)'), :]
        
        if current:
            
            def clock_to_current(elem):
                
                time = [int(num) for num in elem.split(":")]
                current = round(time[0] + (time[1] /60), 2)
                
                return current
            
            for col in self.df.columns:
                self.df[col] = self.df[col].apply(lambda elem: clock_to_current(elem))
                
        self.df.index = pd.to_datetime(self.df.index.get_level_values(0))
            
        return self.df
        
        
df = pd.concat([select_parameter("Fortaleza2014.2.txt").peak(), 
                EPBsEvents()], axis = 1)
df.to_csv("EPBsEventsAndPRE_Fortaleza2014.2.txt", 
          index = True, sep = " ")
        






