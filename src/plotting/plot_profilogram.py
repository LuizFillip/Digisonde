# -*- coding: utf-8 -*-
"""
Created on Wed May 24 12:38:10 2023

@author: Luiz
"""

import matplotlib.pyplot as plt


ds = pd.pivot_table(
    df, 
    index = "alt", 
    values = "freq", 
    columns = df.index
    ).interpolate()

plt.contourf(ds.columns, ds.index, ds.values, 
             50, cmap = "jet")

plt.show()

