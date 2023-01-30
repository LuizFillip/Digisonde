import pandas as pd
import matplotlib.pyplot as plt
import os
from PRE import drift
from core import iono_frame
from utils import smooth



df = pd.read_csv("database/drift/016.txt", index_col = 0)
df.index = pd.to_datetime(df.index)
df = df.loc[df.index.hour >=18]

x = df.index
y = df["17"].values

plt.plot(x, y)

plt.plot(x, smooth(y, 3), 'r-', lw=2)

#%%
infile = "database/process/SL_2014-2015/"

_, _, files = next(os.walk(infile))

filename = files[0]


df1 = drift(iono_frame(infile + 
                       filename).sel_day_in(day = 16))


fig, ax = plt.subplots()

df1[[6, 7, 8]].plot(ax = ax)


