import datetime as dt
import base as b 
import os


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


def path_ionogram(dn, target = None, site = 'SAA0K', root = 'E:\\'):
    folder_ion = dn.strftime('%Y%m%d')
    
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
            closest_dn = closest_iono(target, path_in )
        
        filename = closest_dn.strftime(f'{site}_%Y%m%d(%j)%H%M%S.PNG')
        
        return site, f'{path_in}{filename}'
    
dn = dt.datetime(2014, 1, 2, 21)
# target =  dt.datetime(2014, 1, 3, 3)
# path_ionogram(dn, target = None, site = 'SAA0K')

