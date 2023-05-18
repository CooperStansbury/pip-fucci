import sys
import re
import yaml
from pathlib import Path
import pandas as pd
import numpy as np
from pathlib import Path
from tifffile import imread
from tifffile import imwrite

def getIntensityImage(img, labels=None):
    """ If labels are passed, the image will be masked at each 
    time point to exclude cell regions from background intensity """
    c,t, y, x = img.shape
    xy = x * y
    img2 = img.reshape(t, xy, c)
    if labels is None:
        return img2
    else:
        labelIm2 = labels.reshape(t, xy)
        mask = np.where(labelIm2 > 0, 1, 0)
        mask_3d = np.stack((mask,mask,mask),axis=2) #3 channel mask
        img2 = np.where(mask_3d==1, img2, np.nan)
        return img2
    
    
def getIntensityStats(getIntensityImage):
    """A function to compute mean, std for each time point"""
    
    res = []
    
    for t in range(getIntensityImage.shape[0]):
        for c in range(getIntensityImage.shape[2]):
                H = getIntensityImage[t, :, c]
                
                row = {
                    't' : t,
                    'c' : c,
                    'mean' : np.nanmean(H),
                    'std' : np.nanstd(H),
                    'size' : H.size,
                }

                res.append(row)

    res = pd.DataFrame(res)
    return res

if __name__ == "__main__":    
    imgPath = sys.argv[1]
    backPath = sys.argv[2]

    # read images
    img = imread(imgPath)
    
    # get background 
    intImg = intensityImage = getIntensityImage(img)
    
    # get the summary statistics 
    idf = getIntensityStats(intImg)

    # save files
    idf.to_csv(backPath, index=False)
