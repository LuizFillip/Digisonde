import locale
import matplotlib.pyplot as plt

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
fontsize = 30

lw = 1
major = 8
minor = 4
plt.rcParams.update({'font.size': fontsize, 
                     'axes.linewidth' : lw,
                     'grid.linewidth' : lw,
                     'lines.linewidth' : lw,
                     'legend.frameon' : False,
                     'savefig.bbox' : 'tight',
                     'savefig.pad_inches' : 0.05,
                     'mathtext.fontset': 'dejavuserif', 
                     'font.family': 'serif', 
                     'ytick.direction': 'in',
                     'ytick.minor.visible' : True,
                     'ytick.right' : True,
                     'ytick.major.size' : lw + major,
                     'ytick.major.width' : lw,
                     'ytick.minor.size' : lw + minor,
                     'ytick.minor.width' : lw,
                     'xtick.direction' : 'in',
                     'xtick.major.size' : lw + major,
                     'xtick.major.width': lw,
                     'xtick.minor.size' : lw + minor,
                     'xtick.minor.width' :lw,
                     'xtick.minor.visible' : True,
                     'xtick.top' : True,
                     'axes.prop_cycle' : 
                    plt.cycler('color', ['#0C5DA5', '#00B945', '#FF9500', 
                                                              '#FF2C00', '#845B97', '#474747', '#9e9e9e'])
                         }) 
    
    
