import pandas as pd
import os
import digisonde as dg


def process_day(infile, 
                ext = "DVL", 
                save_in = "20131.txt"):
    
    
   files = [f for f in os.listdir(infile) 
            if f.endswith(ext)]
   out = []
   for filename in files:
       
        out.append(dg.load_export(
            os.path.join(infile, filename)
            ))
        
  
   return  pd.concat(out)

def process_year(main_path):

    main_path = 'D:\\drift\\SAA\\2013\\'
    
    files = os.listdir(main_path)
    
    out = []
    
    for folder in files:
            
        try:
            out.append(process_day(os.path.join(main_path, folder)))
        except:
            
            continue
        
    df = pd.concat(out)
    
    df.to_csv('2013_drift.txt')
    
    return df


