import pandas as pd
import numpy as np
from FabryPerot.core import FabryPerot, resample_interpolate
from build import paths as p
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import datetime as dt


def func(x, a, c):
    return a * x + c


drift_file = p("Drift").get_files_in_dir("SSA")


df = pd.read_csv(drift_file[1], index_col = 0)
df.index = pd.to_datetime(df.index)

df = df.loc[(df["vx"] > -200), :]



df = df.resample("5min").last().interpolate()


fpi_file = p("FabryPerot").get_files_in_dir("processed")


df1 = pd.read_csv(fpi_file, index_col = 0)

df1.index = pd.to_datetime(df1.index)

df1 = df1.loc[(df1["zon"] > -200), :]


date = dt.time(22, 0, 0)

col1 = "vx"
col2 = "mer"



df21 = df.loc[df.index.time == date, [col1]]

df12 = df1.loc[df1.index.time == date, [col2]]


join = pd.concat([df21 , df12], axis = 1).dropna()

join = join.loc[~(df["vy"] < -200), :]


fig, ax = plt.subplots()


xdata = join[col1].values
ydata = join[col2].values


ax.plot(xdata, ydata, 
         linestyle = "none", marker = "o")

lim = 200

ax.set(ylabel = "FPI", xlabel = "DRIFT", 
       ylim = [-lim, lim],
       xlim = [-lim, lim],
       title = f"Meridional - {date}")


popt, pcov = curve_fit(func, xdata, ydata)

ax.grid()
ax.plot(xdata, func(xdata, *popt), 'r-',
         label='fit: a=%5.3f, c=%5.3f' % tuple(popt))

ax.legend()
