import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import setup as s

site = "Sao luis"

name = site.replace(" ", "_")
infile = f"database/counts/{name}_2013_2023.txt"

fig, ax = plt.subplots(figsize = (10, 4))

s.config_labels()

df = pd.read_csv(infile, index_col = 0)

img = ax.imshow(df.values, 
                aspect = "auto", 
                cmap = "Blues", 
                vmax = 144)

ax.set_xticks(np.arange(0, 365, 30))

ax.set_yticks(np.arange(len(df.index)), 
              labels = df.index)

ax.set(ylabel = "Anos", 
       xlabel = "Dias", 
       title = f"Velocidade de deriva - {site}")

s.colorbar_setting(img, ax, 
                   ticks = np.arange(0, 150, 20),
                   label = "# dados por dia")

plt.show()
