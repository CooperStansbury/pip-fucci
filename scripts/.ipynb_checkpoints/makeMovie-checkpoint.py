import sys
import yaml
import pandas as pd
import numpy as np
from pathlib import Path
from tifffile import imread
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import matplotlib.colors as clt
from skimage.segmentation import find_boundaries


def buildCmap(config):
    """A function to build a binary colormap with
    transparency """
    color = config['segmentation_movie']['seg_color']
    c1 = clt.colorConverter.to_rgba('white', alpha = 0)
    c2 = clt.colorConverter.to_rgba(color, alpha = 1)

    bcmap = clt.LinearSegmentedColormap.from_list('cmap', [c1,c2], 512)
    return bcmap


def makeMovie(img, seg, channelMapper, config, outpath):
    """A function to animate the segmentation 
    results """

    # set up the image
    fps = config['segmentation_movie']['fps']
    dpi = config['segmentation_movie']['dpi']
    h = config['segmentation_movie']['height']
    w = config['segmentation_movie']['width']
    
    plt.rcParams['figure.dpi'] = dpi
    plt.rcParams['figure.figsize'] = h, w

    fig, ax = plt.subplots(1, 3)

    # set up the overlay colormap
    bcmap = buildCmap(config)

    images = []
    for t in range(img.shape[1]):
        
        frame = []
        # get the segmentation edges as a binary image
        bounds = np.where(find_boundaries(seg[t, :, :]), 1, 0)

        # loop through each color channel
        for c in range(img.shape[0]):
    
            # add the processed image
            im = ax[c].imshow(img[c, t, :, :], 
                              animated=True,
                              cmap=channelMapper[c],
                              vmin=0, 
                              vmax=230,
                              zorder=1)
            
            im.axes.set_xticks([])
            im.axes.set_yticks([])
            frame.append(im)
    
            # add the segmentation overlay
            sim = ax[c].imshow(bounds, 
                               cmap=bcmap,
                               zorder=5)
    
            sim.axes.set_xticks([])
            sim.axes.set_yticks([])
    
            frame.append(sim)

        # annotate with the frame number
        annot = ax[0].text(1, 2, f"{t=}", 
                           horizontalalignment='center', 
                           verticalalignment='bottom',
                           zorder=10,
                           bbox=dict(facecolor='lightgrey', 
                                     edgecolor='k', 
                                     pad=2))
    
        frame.append(annot)
        images.append(frame)
    
    ani = animation.ArtistAnimation(fig, 
                                    images, 
                                    interval=50, 
                                    blit=True,
                                    repeat_delay=1000)
    
    ani.save(outpath, writer=PillowWriter(fps=fps))


if __name__ == "__main__":
    imgPath = sys.argv[1]
    segPath = sys.argv[2]
    configPath = sys.argv[3]
    outpath = sys.argv[4] 

    img = imread(imgPath)
    seg = imread(segPath)
    
   # load the config for any processing params
    config = yaml.safe_load(Path(configPath).read_text())

   # define the color scheme from the channel index
    colors = {
        'nucleus' : 'Blues',
        'red' : 'Reds',
        'green' : 'Greens',
    }
    
    channelMapper = dict((v, colors[k]) for k,v in config['channels'].items()) 

    # do the work
    makeMovie(img, seg, channelMapper, config, outpath)


    
    