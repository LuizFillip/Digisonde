import datetime as dt


embrace_infos = {
    "FZA0M": "Fortaleza",
    
    "SAA0K": "São Luis", 
    
    "BLJ03": "Belem", 
    
    "BVJ03": "Boa Vista",
    
    "CGK21": "Campo Grande",
    
    "CAJ2M": "Cachoeira Paulista",
    
    "SMK29": "Santa Maria",
    }

def get_infos(filename):
    
    """Getting EMBRACE sites informations by filename"""
    
    keys = embrace_infos.keys()
    f = filename.split("_")
    for key in keys:
        if (key == f[0]):
            name = embrace_infos[key]["name"]
            lat = embrace_infos[key]["lat"]
            lon = embrace_infos[key]["lon"]
            return name, lat, lon

def site_datetime_from_file(file, hours = 21):
    
    args = file.split('_')
    
    dn = dt.datetime.strptime(
        args[-1].split('.')[0], '%Y%m%d(%j)'
        )
    delta = dt.timedelta(hours = hours)
    return args[0][:3].lower(), dn + delta


# filename = 'CAJ2M_20220724(205).TXT'

