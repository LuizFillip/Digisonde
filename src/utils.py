import datetime as dt
import base as b 
import os


def dn2fn(dn, site):
    return dn.strftime(f'{site}_%Y%m%d(%j).TXT')

def fn2dn(filename):
    
    args = filename.split("_")
    
    try:
        date_str = args[1][:8] + args[1][13:-4]
        fmt =  "%Y%m%d%H%M%S"
        return dt.datetime.strptime(date_str, fmt)
    
    except:
        date_str = args[1].split('.')[0]
        fmt = "%Y%m%d(%j)%H%M%S"
        return dt.datetime.strptime(date_str, fmt)

        
def closest_iono(target, path_in):
    iono_times = [
        fn2dn(f) for f in
        os.listdir(path_in) if 'PNG' in f ]
  
    return b.closest_datetime(iono_times, target)

def code_name(code):
    codes = {
        'JI91J': 'Jicamarca',
        "FZA0M": "Fortaleza",
        "SAA0K": "São Luis", 
        "BLJ03": "Belem", 
        "BVJ03": "Boa Vista",
        "CGK21": "Campo Grande",
        "CAJ2M": "Cachoeira Paulista",
        "SMK29": "Santa Maria",
        }
    return codes[code]
    

def path_ionogram(
        dn, 
        target = None, 
        site = 'SAA0K', 
        root = 'E:\\'
        ):
    folder_ion = dn.strftime('%Y/%Y%m%d')
    
    path = os.path.join(root, 'ionogram', folder_ion)
    
    if target is None:
        return f'{path}{site[0]}/'
        
    else:
        try:
            path_in = f'{path}S/'
            site = 'SAA0K' 
            closest_dn = closest_iono(target, path_in)
        except:
            path_in = f'{path}F/'
            site = 'FZA0M'
            closest_dn = closest_iono(target, path_in)
        
        fmt = f'{site}_%Y%m%d(%j)%H%M%S.PNG'
        filename = closest_dn.strftime(fmt)
        
        return site, f'{path_in}{filename}'
    
# dn = dt.datetime(2018, 12, 12)

# path_ionogram(dn)