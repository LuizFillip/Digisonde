import cv2
import os
import matplotlib.pyplot as plt
from utils import ionosonde_fname    


def crop_image(file, y = 50, x = 130, h = 900, w = 750):
    img = cv2.imread(file)
    return img[y: y + h, x: x + w]

def setting_image_labels(img, 
                         filename, 
                         site = "Fortaleza", 
                         width = 10, 
                         height = 10, 
                         path_to_save = "",
                         save = False):
    
    if save:
        plt.ioff()
    
    fig, ax = plt.subplots(figsize = (width, height))
    
    date_time = ionosonde_fname(filename)
    
    ax.imshow(img)
    
    ax.text(80, 50, f"{date_time.time()} UT", 
        transform = ax.transData, 
        color = "white", fontsize = 20)

    ax.text(400, 50, f"{date_time.date()}", 
        transform = ax.transData, 
        color = "white", fontsize = 20)

    ax.set(xticks = [], yticks = [], title = site)
    
    if save:
        print("saving...", filename)
        fig.savefig(path_to_save + filename, 
                    dpi = 100, 
                    bbox_inches = "tight", 
                    transparent = True)
    else:
        plt.show()
        
def main():
    infile = "G:\\My Drive\\Python\\data-analysis\\digisonde\\img\\2014\\"
    
    _, _, files = next(os.walk(infile))
    
    path_to_save = "G:\\My Drive\\Python\\data-analysis\\digisonde\\img\\2014_test\\"
    
    
    for filename in files:
        crop_img = crop_image(infile + filename)
        setting_image_labels(crop_img, filename, 
                             path_to_save = path_to_save, 
                             save = True)