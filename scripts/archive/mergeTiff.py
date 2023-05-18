import sys
import re
import yaml
from pathlib import Path
import pandas as pd
import numpy as np
from pathlib import Path
from tifffile import imread
from tifffile import imwrite
from skimage.color import rgb2gray
from skimage.transform import rescale



if __name__ == "__main__":
    outpath = sys.argv[1]
    filePaths = sys.argv[2:]  # a list of file paths, note the colon
    
    """The file must have a temporal ID assigned by the pipeline"""
    
    fileList = []
    tList = []
    
    for fpath in filePaths:
        
        # get the timepoint id from filename
        t = int(re.sub('\D', '', fpath.split("_")[-1]))

        # load the full image
        img = imread(fpath)
        
        tList.append(t)
        fileList.append(img)
        
    
    # sort the image array by time
    sortInd = np.argsort(tList)
    imgArr = np.asarray(fileList)
    imgArr = imgArr[sortInd, :, : ,:]
    
    imwrite(outpath, imgArr)