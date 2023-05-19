import sys
import re
import yaml
from pathlib import Path
import pandas as pd
import numpy as np
from pathlib import Path


def getAhat(tracks, config):
    """A function to compute the corrected aplha
    value using Bonferroni correction """
    alpha = config['phase']['alpha']

    # number of tests performed is one per cell per time for each channel
    t = tracks[['t', 'label']].drop_duplicates()
    ntests = len(t) * 3
    alphaHat = 1 - ((1-alpha) ** (1/ntests))
    print(f"{alpha=} {ntests=} {alphaHat}")
    return alphaHat


def getPhases(tracks, config):
    """A function to threhold pvals """
    a = getAhat(tracks, config)

    testCols = [
        'c0_pval_prepared',
        'c0_pval_processed',
        'c1_pval_prepared',
        'c1_pval_processed',
        'c2_pval_prepared',
        'c2_pval_processed',
    ]

    # threshold all based on corrected alpha
    flags = np.where(tracks[testCols] <= a, 1, 0)
    flags = pd.DataFrame(flags, columns=testCols)
    flags = flags.fillna(0)

    newCols = ['c0', 'c1', 'c2']

    # cell must be significant in both 
    # the processed and raw images
    for c in newCols:
        pairs = [x for x in flags.columns if c in x]
        flags[c] = flags[pairs].min(axis=1)
        # print(c, pairs)

    
    flags = flags[newCols].astype(str)
    flags['val'] = flags.agg(''.join, axis=1)

    # map phases
    phaseMap = config['phase']['phase_map']
    phaseMap_r = dict((v,k) for k,v in phaseMap.items())
    
    tracks['phase'] = flags['val'].map(phaseMap_r)
    tracks['phase'] = tracks['phase'].fillna('NA')
    return tracks



if __name__ == "__main__":
    tracks = pd.read_csv(sys.argv[1])
    configPath = sys.argv[2]
    outpath = sys.argv[3]

    # load the config for any processing params
    config = yaml.safe_load(Path(configPath).read_text())
    
    phased = getPhases(tracks, config)
    phased.to_csv(outpath, index=False)
    
        