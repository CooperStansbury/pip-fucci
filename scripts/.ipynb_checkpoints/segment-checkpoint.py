import sys
import yaml
from pathlib import Path
import pandas as pd
import numpy as np
from pathlib import Path
from itertools import repeat
from tifffile import imread
from tifffile import imwrite
import skimage
import math
import multiprocessing

# define the environment for stardist
from stardist.models import StarDist2D
from csbdeep.utils import normalize
from skimage.measure import regionprops
from skimage.exposure import rescale_intensity


def getCircularity(region):
    if region.perimeter > 0:
        circularity = 4*math.pi * (region.area / region.perimeter**2)
    else: 
        circularity = 0
    return circularity
    

def getRegionPropsTable(properties, intensities=True):
    """A function to get the region props for multiple segmentations"""
    propTable = []
    for segment in properties:
        if intensities:
            intens = segment.image_intensity
        else:
            intens = None
            
        row = {
            'area' : segment.area,
            'area_convex' : segment.area_convex,
            'area_filled' : segment.area_filled,
            'axis_major_length' : segment.axis_major_length,
            'axis_minor_length' : segment.axis_minor_length, 
            'centroid_y' : segment.centroid[0],
            'centroid_x' : segment.centroid[1],
            'eccentricity' : segment.eccentricity,
            'intensity' : intens, # full distribution of intensities
            'intensity_max' : segment.intensity_max,
            'intensity_min' : segment.intensity_min,
            'intensity_mean' : segment.intensity_mean,
            'label' : segment.label,
            'orientation' : segment.orientation,
            'perimeter': segment.perimeter,
            'solidity': segment.solidity,
            'slice': segment.slice,
            'circularity' : getCircularity(segment),
        }
        propTable.append(row)
        
    propTable = pd.DataFrame(propTable)
    return propTable


def getIntesityStats(propTable):
    """A function to get distribution of intensities for each 
    segmented cell """
    res = []
    
    for idx, row in propTable.iterrows():
        H = row['intensity']
        
        for c in range(H.shape[2]):
            newRow = {
                't' : row['t'],
                'c' : c,
                'label' : row['label'],
                'mean' : np.nanmean(H[:, :, c]),
                'std' : np.nanstd(H[:, :, c]),
                'size' : H[:, :, c].size,
            }
            res.append(newRow)
  
    res = pd.DataFrame(res)
    return res


def segment(img, config):
    """a customizable function segment images """
    # get the nuclear channel position
    nChan = config['channels']['nucleus']
    
     # configure the pre-trained model
    starDistmodel = config['stardist']['model']
    
    # define the model args
    model = StarDist2D.from_pretrained(starDistmodel)
    prob_thresh = config['stardist']['prob_thresh']
    nms_thresh = config['stardist']['nms_thresh']
    
    
    propTable = []
    segmentation = []
    
    # safe to assume image structure is (time, channel, y, x)
    for t in range(img.shape[1]):    
        # resturcture the input
        nucImg = img[nChan, t, :, :].copy()
        nucImg = normalize(nucImg)
    
        labels, _ = model.predict_instances(nucImg, 
                                            prob_thresh=prob_thresh,
                                            nms_thresh=nms_thresh)
        
        print(f"{t=} {len(np.unique(labels))} cells with prob: {prob_thresh}")
        
        # get the intensity frames
        intImg = img[:, t, :, :].copy()
        intImg = np.swapaxes(intImg, 0, 2)
        intImg = np.swapaxes(intImg, 0, 1)

        # get segmentation metadata
        props = regionprops(labels, intensity_image=intImg)
        pdf = getRegionPropsTable(props)
        pdf['t'] = t # temporal id
        
        propTable.append(pdf)
        segmentation.append(labels)
        
    propTable = pd.concat(propTable)
    segmentation = np.asarray(segmentation)
    
    return propTable, segmentation
    
    
        
if __name__ == "__main__":
    imgPath = sys.argv[1]
    configPath = sys.argv[2]
    imgOutpath = sys.argv[3] 
    dataOutpath = sys.argv[4] 
    intensityOutpath = sys.argv[5] 
    
    # load the config for any processing params
    config = yaml.safe_load(Path(configPath).read_text())
    
    # load the image 
    img = imread(imgPath)
    
    # segment each image slice 
    propTable, segmentation = segment(img, config)
    
    # get cell intensities
    idf = getIntesityStats(propTable)
    
    # save segmentation
    imwrite(Path(imgOutpath), segmentation)
    
    # save results
    propTable.to_csv(Path(dataOutpath), index=False)
    
    # save intensities
    idf.to_csv(Path(intensityOutpath), index=False)

    