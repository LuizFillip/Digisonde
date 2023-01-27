import datetime as dt

class ionosonde_fname(object):

    def __init__(self, filename):
    
        args = filename.split("_")
    
        self.code = args[0]
    
        self.date = args[1][:8]
    
        self.time = args[1][13:-4]
        
        str_datetime = self.date + self.time
    
        self.datetime = dt.datetime.strptime(str_datetime, 
                                             "%Y%m%d%H%M%S")