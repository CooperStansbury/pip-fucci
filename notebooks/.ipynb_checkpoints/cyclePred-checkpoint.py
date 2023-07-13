import pandas as pd
import numpy as np


def getAhat(tracks, alpha):
    """A function to compute the corrected aplha
    value using Bonferroni correction """

    # number of tests performed is one per cell per time for each channel
    t = tracks[['t', 'label']].drop_duplicates()
    ntests = len(t) * 3
    alphaHat = 1 - ((1-alpha) ** (1/ntests))
    print(f"{alpha=} {ntests=} {alphaHat}")
    return alphaHat


def getPhases(tracks, alpha, correct=True):
    """A function to threhold pvals """
    if correct:
        a = getAhat(tracks, alpha)
    else:
        a = alpha

    testCols = [
        'c0_pval_processed',
        'c2_pval_processed',
    ]

    # threshold all based on corrected alpha
    flags = np.where(tracks[testCols] <= a, 1, 0)
    flags = pd.DataFrame(flags, columns=testCols)
    flags = flags.fillna(0)

    newCols = ['c0','c2']

    # cell must be significant in both 
    # the processed and raw images
    for c in newCols:
        pairs = [x for x in flags.columns if c in x]
        flags[c] = flags[pairs].min(axis=1)
        # print(c, pairs)

    
    flags = flags[newCols].astype(str)
    flags['val'] = flags.agg(''.join, axis=1)

    phaseMap_r = {
        "10" : "G1",
        "11" : "G1/S",
        "01" : "S/G2/M",
    }
    
    tracks['phase'] = flags['val'].map(phaseMap_r)
    tracks['phase'] = tracks['phase'].fillna('NA')
    return tracks