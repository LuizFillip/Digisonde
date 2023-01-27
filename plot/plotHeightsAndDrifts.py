import matplotlib.pyplot as plt
import os
from pipeline import iono_frame
from plotConfig import *

infile = "database/process/"

_, _, files = next(os.walk(infile))

filename = files[0]

df = iono_frame(infile, filename).sel_day_in(day = 1)


fig, ax = plt.subplots(figsize = (15, 10), nrows = 2)
freqs = list(df.columns[1:])
df[freqs].plot(ax = ax[0])


