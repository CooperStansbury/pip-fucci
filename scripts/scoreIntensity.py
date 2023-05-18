import sys
import re
import yaml
from pathlib import Path
import pandas as pd
import numpy as np
from pathlib import Path
from tifffile import imread
from tifffile import imwrite
import scipy 
from ast import literal_eval


def _test(row):
    """a lambda apply function to return test values """
    cellMean = row[0]
    cellStd = row[1]
    cellN = row[2]
    bckgrndMean = row[3]
    bckgrndStd = row[4]
    bckgrndN = row[5]
    
    _, pval = scipy.stats.ttest_ind_from_stats(cellMean, 
                                               cellStd, 
                                               cellN, 
                                               bckgrndMean, 
                                               bckgrndStd,
                                               bckgrndN,
                                               equal_var=False, 
                                               alternative='greater')
    return pval


def _foldChange(row):
    """A lambda apply function to compute the fold change of 
    cell intensity against the background """
    cellMean = row[0]
    bckgrndMean = row[3]
    lfc = np.log1p(cellMean) - np.log1p(bckgrndMean)
    return lfc


def testIntensities(cells, background):
    """A function to statistically test the presence of flourescent 
    markers """
    
    # merge the intensities with the cell segementations
    df = pd.merge(cells, background,
                  how='left', 
                  left_on=['t', 'c'],
                  right_on=['t', 'c'],
                  suffixes=('_cell', '_bckgnd'))
    
    testCols = [
        'mean_cell',  
        'std_cell', 
        'size_cell',
        'mean_bckgnd',
        'std_bckgnd',
        'size_bckgnd',   
    ]
    
    df['pval'] = df[testCols].apply(lambda x: _test(x), axis=1)
    df['logFoldChange'] = df[testCols].apply(lambda x: _foldChange(x), axis=1)
    
    keepcols = [
        't',
        'c',
        'label',
        'pval',
        'logFoldChange',
        'mean_cell',
        'mean_bckgnd',
    ]
    
    return df[keepcols]
    

if __name__ == "__main__":    
    inten = pd.read_csv(sys.argv[1])

    # read background files
    bk = pd.read_csv(sys.argv[2])

    outpath = sys.argv[3]

    # normal background
    scores = testIntensities(inten, bk)
    scores.to_csv(outpath, index=False)

    
 