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
    
    
def getIntensityStats(intImg):
    """A function to compute mean, std for each time point.
    
    NOTE: expects:
        (channel, time, y, x)
    """
    
    res = []
    
    for t in range(intImg.shape[1]):
        for c in range(intImg.shape[0]):
                H = intImg[c, t, :, :]
                
                row = {
                    't' : t,
                    'c' : c,
                    'mean' : np.mean(H),
                    'std' : np.std(H),
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
    print(f"{img.shape=}")

    """DEPRECATED: do not need the full distribution anymore,
    too slow and summmary stats suffice """
    # # get background 
    # intImg = getIntensityImage(img)
    # print(f"{intImg.shape=}")
    
    # get the summary statistics 
    idf = getIntensityStats(img)

    # save files
    idf.to_csv(backPath, index=False)
