import datetime as dt



def site_datetime_from_file(file, hours = 21):
    
    args = file.split('_')
    
    
    delta = dt.timedelta(hours = hours)
    return args[0][:3].lower(), dn + delta



