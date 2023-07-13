import pandas as pd
import numpy as np
import os
import cv2
import sys
import math
import matplotlib
import matplotlib.pyplot as plt
from tifffile import imread
from glob import glob
from scipy.stats import mode
from collections import Counter
import math
import skimage
import re
from itertools import chain
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from functools import partial
import matplotlib.animation as animation
import networkx as nx
from tifffile import imread


def get_wound_area(img, foot=skimage.morphology.square, t=0.5, q=2, dilation=[20, 10, 15]):
    """A function explode the cell areas from an un-segmented, processed image

    Params:
    ------------
    img (np.array):
        The input image
    foot (skimage.morphology.[element]):
        A valid structuring element from `skimage.morphology'
    t (float):
        The scale factor for small object removal, assumes circular footprint
    q (float):
        The scale factor for small hole filling, assumes circular footprint
    dialtion (iterable):
        The different size of the footprint used for image dilation

    Returns:
    ------------
    newImg (np.array):
        Binary image with the wound area
    """
    newImg = img.copy()
    
    # dilate the image
    for r in dilation:
        newImg = skimage.morphology.dilation(newImg, footprint=foot(r))

        # remove single blobs
        min_size = t * (math.pi * (r**2))
        max_hole = q * (math.pi * (r**2))
        newImg = newImg.astype(bool)
        newImg = skimage.morphology.remove_small_holes(newImg, max_hole)
        newImg = skimage.morphology.remove_small_objects(newImg, min_size=min_size)

    newImg = np.invert(newImg)
    return newImg