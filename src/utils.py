import datetime as dt
import base as b 
import os

root = 'E:/ionogram/'


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
        root = 'E:\\ionogram'
        ):
    
    '''
    Reescrever no novo layout 
    
    '''
    folder_ion = dn.strftime('%Y/%Y%m%d')
    
    path = os.path.join(root, folder_ion)
    
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
        
    
        filename = dn2PNG(closest_dn, site)
        return site, f'{path_in}{filename}'
    





def ionogram_path(dn, site, root = 'E:\\'):
    
    start = dn - dt.timedelta(days = 1)
    folder_ion = start.strftime(f'%Y/%Y%m%d{site[0]}')
    
    fmt = f'{site}_%Y%m%d(%j)%H%M%S.PNG'
    
    target = dn.strftime(fmt)
    
    return os.path.join(root, 'ionogram', folder_ion, target)

