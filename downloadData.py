import requests 
from tqdm import tqdm
from bs4 import BeautifulSoup 
import time
from plotVerticaldrift import *
import os



def downloadData(output_path, year, day):
    
    url = f"https://embracedata.inpe.br/ionosonde/FZA0M/{year}/{day}/"
    
    read_html = requests.get(url)
    s = BeautifulSoup(read_html.text, "html.parser")
    
    #print(s)
    
    for link in s.find_all('a', href=True):
        #Find hiperlinks in html parser text
        href = link['href']
        
        matches = [".SAO"]#".RSF", ".PNG"]

        if any(x in href for x in matches):
        #if specify_link in href:
            
            remote_file = requests.get(url + href)
            total_length = int(remote_file.headers.get('content-length', 0))
            chunk_size = 1024
            print(link)
            
            #year_path = create_a_directory(output_path, year)
            #day_path = create_a_directory(year_path, day)
            
            #path_to_save = f"{day_path}{href}"
    
            path_to_save = f"{output_path}{href}"            
            with open(path_to_save, 'wb') as file, tqdm(
                    desc= "Downloading",
                    total = total_length,
                    unit='iB',
                    unit_scale = True,
                    unit_divisor = chunk_size,
            ) as bar:
                for chunk in remote_file.iter_content(chunk_size = chunk_size): 
                    if chunk: 
                        size = file.write(chunk)   
                        bar.update(size) 
                        

def create_a_directory(output_path, number):
    #global new_path
    
    try:
        if int(number) > 366:
            new_path = f"{output_path}{number}\\"
        else:
            new_path = f"{output_path}\\{number}\\"
            
        os.mkdir(new_path)
        
        #conditions for the folder created 
    except OSError:
        #For the case of directory already exists
        print(f"Creation of the directory {number} failed")
    else:
       pass     
    
    return new_path


