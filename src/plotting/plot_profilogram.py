import matplotlib.pyplot as plt


def plot_profilogram(df):


    ds = pd.pivot_table(
        df, 
        index = "alt", 
        values = "freq", 
        columns = df.index
        ).interpolate()
    
    plt.contourf(ds.columns, ds.index, ds.values, 
                 50, cmap = "jet")
    
    plt.show()
    
