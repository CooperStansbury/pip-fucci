import sys
import yaml
from pathlib import Path
import pandas as pd
import numpy as np
from pathlib import Path
from tifffile import imread
from tifffile import imwrite
import skimage


def preprocess(img, config):
    """a customizable function to prepare images
    for segmentation """
    
    from skimage.restoration import rolling_ball
    from skimage.exposure import equalize_adapthist
    from skimage.filters import rank
    from skimage.morphology import disk
    from skimage.filters import median
    from skimage.util import img_as_ubyte
    
    params = config['preprocessing']
    
    # do each channel separately
    for c in range(img.shape[0]):
        
        cImg = img[c, :, :].copy()
        
        # MEDIAN FILTER
        p = params['median_radius']
        if p > 0:
            ft = disk(p)
            cImg = median(cImg, footprint=ft)
        
        # GLOBAL HISTOGRAM EQUALIZATION
        p = params['global_histogram_limit']
        if p > 0:
            cImg = equalize_adapthist(cImg, clip_limit=p)
        
        # BACKGROUND SUBTRACTION
        p = params['bkgnd_radius']
        if p > 0:
            bkgnd = rolling_ball(cImg, radius=p)
            cImg = cImg - bkgnd
            
        # LOCAL HISTOGRAM EQUALIZATION
        p = params['local_histogram_footprint']
        if p > 0:
            ft = disk(p)
            cImg = img_as_ubyte(cImg)
            cImg = rank.equalize(cImg, footprint=ft)

        # resave the processed image
        img[c, :, :] = cImg

    return img
        
    


if __name__ == "__main__":
    imgPath = sys.argv[1]
    configPath = sys.argv[2]
    outpath = sys.argv[3] # single item outpath
    
    # load the config for any processing params
    config = yaml.safe_load(Path(configPath).read_text())

    
    # load the image slice
    img = imread(imgPath)
    
    # process the image slice
    img = preprocess(img, config)
    imwrite(outpath, img)

    