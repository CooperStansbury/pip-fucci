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
from skimage.exposure import rescale_intensity
from multiprocessing import Pool


def getInputs(img, config):
    """A function to prepare images for multiprocessing """
    time = img.shape[1]
    args = []
    for t in range(time):
        img_t = img[:, t, :, :, :]
        tup = (img_t, config.copy(), t)
        args.append(tup)
    return args


def prepareImage(img_t, config, t):
    """A function to prepare the image for downstream preprocessing 

    Notes: 
        - time is assumed to be the second dimension
        - works on a single image at a time
        - flattens RGB and rescales
    """
    sf = config['prepare']['rescale_factor'] # scale factor
    newImg = []

    # process all channel separately
    for c in range(img_t.shape[0]):
        n_img = img_t[c, :, :].copy()
        n_img = rgb2gray(n_img)
        n_img = rescale(n_img, 
                        (sf, sf),
                        anti_aliasing=False)
        
        n_img = rescale_intensity(n_img, out_range=(0, 255))
        newImg.append(n_img)

    newImg = np.asarray(newImg)
    return [t, newImg]
    

if __name__ == "__main__":
    imgPath = sys.argv[1]
    configPath = sys.argv[2]
    outpath = sys.argv[3] # single item outpath

    # load the config for processing params
    config = yaml.safe_load(Path(configPath).read_text())

    # load the image 
    img = imread(imgPath)

    # get the multiprocessing argument tuple
    args = getInputs(img, config)

    # set up the worker pool
    workers = int(config['prepare']['workers'])
    pool = Pool(workers) # important when running on OnDemand

    # run the function!
    result = pool.starmap(prepareImage, args)
    result.sort() # import step!

    # make sure that the transformed range (0, 255) is encoded
    # so that it can be properly compressed!
    newImg = np.asarray([x[1] for x in result], dtype='uint16')
    newImg = np.swapaxes(newImg, 0, 1) # swap the time and channel axis

    # save output
    imwrite(outpath, newImg, 
            bigtiff=True,
            compression='lzw',
            bitspersample=config['prepare']['bitspersample'],
           )
    
    