import os
from tqdm import tqdm 

def extract_drift_files():
    infile = "D:\\drift\\SAA\\2013\\"
    ext = "DVL"
    name_to_save = "2013.txt"
    
    out = []
    for day_of_year in os.listdir(infile):
        
        folder_path = os.path.join(infile, day_of_year)
        files = os.listdir(folder_path)
        files = [f for f in files if f.endswith(ext) if len(files) != 0]
        
        for filename in tqdm(files, desc = day_of_year):
            try:
                f = open(os.path.join(folder_path, filename), "r")
                out.append(f.read())
            except:
                continue
            
    res = "".join(out)
    
    def save_results(res, name_to_save):
        text_file = open(name_to_save, "w")
        text_file.write(res)
        text_file.close()
        
    save_results(res, name_to_save)
    
