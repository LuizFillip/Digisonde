import datetime as dt
import base as b
import os 
import shutil
from tqdm import tqdm 



# path_out = 'D:\\drift\\june\\'

# for i in tqdm(range(182)):
    
#     dn = dt.datetime(2023, 1, 1) + dt.timedelta(days = i)
#     doy = dn.strftime('%j')
#     path = f'D:\\drift\\saa\\{dn.year}\\{doy}\\'
#     for file in os.listdir(path):
        
#         if 'XML' in file:
#             os.remove(path + file)
        
#         if file[-3:] == 'SAO':
#             src = path + file
#             dst = path_out + file
#             shutil.move(src, dst)
    
    