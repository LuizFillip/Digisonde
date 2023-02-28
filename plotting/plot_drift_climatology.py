import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from utils import smooth
import setup as s

pd.options.mode.chained_assignment = None

def filter_and_smooth(df):
    
    ts = df.loc[(df["vx"] > -100) & 
                (df["vx"] < 100) &
                (df["vy"] < 200) &
                (df["vy"] > -200) &
                (df["vz"] > -50) &
                (df["vz"] < 80)]
    
    
   


def plotContourf(ax, ts):
    df1 = ts.loc[(ts.index.hour <= 8) |
                 (ts.index.hour >= 20)]
    
    
    df1["time"] = datetime_to_float(df1)
    df1["date"] = df1.index.date
    
    
    res = pd.pivot_table(df1, 
                         values = "vx", 
                         index = "time", 
                         columns = "date")
    
    
    res = res.interpolate()
    
    
    
    X, Y = np.meshgrid(res.columns, res.index)
    
    Z = res.values
    
    img = ax.pcolormesh(X, Y, Z,  
                        cmap = "jet") 
    
    plt.colorbar(img)

def datetime_to_float(res):
    
    hour = res.index.hour + res.index.minute / 60
    return np.where(hour >= 9, hour, hour + 24)






