import datetime as dt
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
        "SMK29": "Santa Maria"
        }
    return codes[code]
    

def dn2fn(dn, site):
    '''
    get filename from date and site name
    '''
    return dn.strftime(f'{site}_%Y%m%d(%j).TXT')



def ionogram_path(dn, site, root = 'E:\\'):
    
    start = dn - dt.timedelta(days = 1)
    folder_ion = dn.strftime(f'%Y/%Y%m%d{site[:2]}')
    
    fmt = f'{site}_%Y%m%d(%j)%H%M%S.PNG'
    
    target = dn.strftime(fmt)
    
    return os.path.join(root, 'ionogram', folder_ion, target)

