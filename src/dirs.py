import os 
import digisonde as dg
import datetime as dt 
import base as b 


def closest_iono(target, path_in):
    iono_times = [
        fn2dn(f) for f in
        os.listdir(path_in) if 'PNG' in f ]
  
    return b.closest_datetime(iono_times, target)


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

def iono_path_from_target(target, site, root = 'E:\\'):
    '''
    Localize o caminho de um arquivo de um ionograma
    (formato PNG) para um tempo de entrada (target)
    de um tempo mais próximo (e.g, imagem do imageador)
    '''
    folder_fmt = f'%Y/%Y%m%d{site[0]}'
    
    folder_ion = target.strftime(folder_fmt)
    
    PATH_IONO = os.path.join(root, 'ionogram', folder_ion)
    
    dn = dg.closest_iono(target, PATH_IONO)
    
    fmt = f'{site}_%Y%m%d(%j)%H%M%S.PNG'
    
    return dn, os.path.join(PATH_IONO, dn.strftime(fmt))
        

class IonoDir(object):
    
    def __init__(self, site, dn):
        
        self.site = site
        self.dn = dn 
        self.root = 'E:/ionogram/'
        self.ext = self.site[:2]
        
    @property
    def name_folder(self):
        fmt = '%Y/%Y%m%d' + self.ext
        return self.dn.strftime(fmt)
    
    @property
    def folder_path(self):
        return f'{self.root}{self.name_folder}'
    
    @property
    def dn2PNG(self):
        fmt = f'{self.site}_%Y%m%d(%j)%H%M%S.PNG'
        return self.dn.strftime(fmt)
    
    @property 
    def list_full_paths(self):
        
        files = os.listdir(self.folder_path)
        
        return [f'{self.folder_path}/{f}' for f in files]
    
    def get_time_list(self, ext = 'PNG'):
        
        files = os.listdir(self.folder_path)
        
        return [fn2dn(f) for f in files if ext in f]
    
    @property 
    def path_from_dn(self):
        
        return f'{self.folder_path}/{self.dn2PNG}'
        
    
  
def test_IonoDir(site, dn):
    p = IonoDir(site, dn)
    
    p.name_folder
