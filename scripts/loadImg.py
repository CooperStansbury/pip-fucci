import sys
import yaml
from pathlib import Path
import pandas as pd
import numpy as np
from pathlib import Path
from tifffile import imread
from tifffile import imwrite
from skimage.color import rgb2gray
from skimage.transform import rescale


def loadDefault(img):
    """A function to load a default image. Any image 
    restructurting would go here..."""
    return img

def flattenRGB(img):
    """A function to get a luminosity image from 3-channel RGB"""
    return rgb2gray(img)

def rescaleSlice(img, scale_factor):
    """A function to rescale a single grey scale slice
    based on the scale factor applied to XY.
    
    NOTE: this is for a slice, we shouldn't downsample the 
    separate channels in position [0] of img.shape
    """
    return rescale(img, (1, scale_factor, scale_factor), anti_aliasing=False)


if __name__ == "__main__":
    imgPath = sys.argv[1]
    configPath = sys.argv[2]
    outpaths = sys.argv[3:]  # a list of file paths, note the colon
    
    # load the config for any processing params
    config = yaml.safe_load(Path(configPath).read_text())
    
    # load the full image
    img = imread(imgPath)
    
    # a blank function for preprocessing, if needed
    # for example, handling differently shaped input
    img = loadDefault(img) 
    
    # loop through each time-point and perform
    # minor restructuring
    for t in range(img.shape[1]):
        img_t = img[:, t, :, :]
        
        if config['flattenRGB']:
            img_t = flattenRGB(img_t)
            
        img_t = rescaleSlice(img_t, config['downsample_scale_factor'])
        
        imwrite(outpaths[t], img_t)

    