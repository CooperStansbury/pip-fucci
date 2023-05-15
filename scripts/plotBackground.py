import sys
import re
import yaml
from pathlib import Path
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


def reformatIntensity(inten):
    """A function to pivot intensities """
    inten = pd.pivot_table(inten, 
                           values=['mean', 'std'], 
                           index=['t', ], 
                           columns='c',)


    inten.columns = inten.columns.to_flat_index()
    inten = inten.reset_index(drop=False)
    return inten


def plotBackground(inten, channelMapper, outpath):
    """A function to build a plots"""
    tMax = inten['t'].max()
    
    # hacky way to resize the image based on the number of 
    # timepoints in the data
    pltoSize = int(1.5*np.log(tMax)), int(0.6 * np.log(tMax))
    
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['figure.figsize'] = pltoSize
    fig, axs = plt.subplots(1, 3, sharey=True)
    axs = axs.ravel()
    
    for k, v in channelMapper.items():
        time = inten['t'].to_list()
        mean = inten[("mean", k)].to_numpy()
        std = inten[("std", k)].to_numpy()

        ub = mean + std
        lb = mean - std

        axs[k].plot(time, mean, c=v, lw=1, zorder=2)
        axs[k].plot(time, ub, c=v, lw=0.5, zorder=1)
        axs[k].plot(time, lb, c=v, lw=0.5, zorder=1)

        axs[k].fill_between(time, ub, lb, 
                            color=v, 
                            alpha=0.5, 
                            zorder=0)
    

        axs[k].set_xlabel("Frame")

    plt.tight_layout()
    sns.despine()
    plt.savefig(outpath, bbox_inches='tight')


if __name__ == "__main__":
    inten = pd.read_csv(sys.argv[1])
    configPath = sys.argv[2]
    outpath =  sys.argv[3]    

    # load the config for any processing params
    config = yaml.safe_load(Path(configPath).read_text())
    
    
    # define the color scheme from the channel index
    colors = {
        'nucleus' : 'C0',
        'red' : 'r',
        'green' : 'g',
    }
    
    channelMapper = res = dict((v,colors[k]) for k,v in config['channels'].items()) 
    
    # reformat the background intensities
    inten = reformatIntensity(inten)
    
    # plot the image 
    plotBackground(inten, channelMapper, outpath)

    
