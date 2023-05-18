import sys
import yaml
from pathlib import Path
import pandas as pd
import numpy as np
from pathlib import Path
from tifffile import imread
from tifffile import imwrite
from skimage.restoration import rolling_ball
from skimage.restoration import denoise_bilateral
from skimage.exposure import equalize_adapthist
from skimage.morphology import disk
from skimage.filters import median
from multiprocessing import Pool
from skimage.exposure import rescale_intensity


def getInputs(img, config):
    """A function to prepare images for multiprocessing """
    time = img.shape[1]
    args = []
    for t in range(time):
        img_t = img[:, t, :, :] # note that this is one fewer dims due to RGB flattening
        tup = (img_t, config.copy(), t)
        args.append(tup)
    return args


def processImage(img_t, config, t):
    """A function to prepare the image for segmentation
    """
    newImg = []

    # process all channels separately
    for c in range(img_t.shape[0]):
        n_img = img_t[c, :, :].copy()

        # median filtering
        m_radius = int(config['preprocess']['median_rad'])
        n_img = median(n_img, np.ones((m_radius, m_radius)))

        # histogram equalization
        h_radius = int(config['preprocess']['adaptive_hist_rad'])
        n_img = equalize_adapthist(n_img, (h_radius, h_radius))

        # denoising
        n_img = denoise_bilateral(n_img)

        # background subtraction
        b_radius = int(config['preprocess']['bkgnd_rad'])
        bkgnd = rolling_ball(n_img, radius=b_radius)
        n_img = n_img - bkgnd

        # make sure data typing is correct
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
    workers = int(config['preprocess']['workers'])
    pool = Pool(workers) # important when running on OnDemand

    # run the function!
    result = pool.starmap(processImage, args)
    result.sort() # import step!

    # make sure that the transformed range (0, 255) is encoded
    # so that it can be properly compressed!
    newImg = np.asarray([x[1] for x in result], dtype='uint8')
    newImg = np.swapaxes(newImg, 0, 1) # swap the time and channel axis

    # save output
    imwrite(outpath, 
            newImg, 
            bigtiff=True,
            photometric='rgb',
            compression='lzw',
            bitspersample=config['prepare']['bitspersample'],
           )
    
    