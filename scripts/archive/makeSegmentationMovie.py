import sys
import re
import yaml
import cv2
from pathlib import Path
import pandas as pd
import numpy as np
from pathlib import Path
from tifffile import imread
from tifffile import imwrite
from skimage.color import rgb2gray
from skimage.transform import rescale



if __name__ == "__main__":
    imgPath = sys.argv[1]
    segPath = sys.argv[2]
    outpath = sys.argv[3]
    
    # load the full image
    img = imread(imgPath)
    seg = imread(segPath)
    
    # get shape
    

    print(f"{img.shape=}")
    print()
    