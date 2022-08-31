# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 10:29:08 2022

@author: Luiz
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import config
from plotAnnualvariation import *
from plotESFaverage import *
from plotIndicators import *






def plotAllparameters(site = "Fortaleza"):
    
    
    fig, ax = plt.subplots(figsize = (10, 12), 
                           nrows = 3, 
                           sharex=(True))

    plt.subplots_adjust(hspace = 0)
    
    plotAnnualvariation(f"Results/{site}/PRE/", 
                        "2014.txt", 
                        site = site, 
                        ax = ax[0])
    
    
    img = plotESFaverage("Database/QF/", ax = ax[1])
    
    cbar_ax = fig.add_axes([.93, 0.38, 0.015, 0.24])
    cb = fig.colorbar(img, 
                      ticks = np.arange(0, 50 + 10, 10), 
                      cax=cbar_ax)
    
    cb.set_label('QF (km)')
    
    plotKp("Database/PlanetaryIndicators/", 
           "Kp_ap_Ap_SN_F107_since_1932.txt", 
                parameter = "Ap", 
                year = 2014, 
                ax = ax[2])
    
    fig.suptitle(site, y = 0.91)
    
    
#plotAllparameters(site = "Fortaleza")