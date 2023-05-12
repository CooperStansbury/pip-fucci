import sys
import re
import yaml
from pathlib import Path
import pandas as pd
import numpy as np
from pathlib import Path
from tifffile import imread
from tifffile import imwrite
import ast

def splitIntensityStats(cells):
    """A function to split intensity values (nested)
    into new columns """
    
    def parse(row):
        return row.replace("[", "").replace("]", "").split()
    
    INTEN_COLUMNS = [
        'intensity_max',
        'intensity_min', 
        'intensity_mean',
    ]
    
    for c in INTEN_COLUMNS:
        # convert to list explicitly
        cells[c] = cells[c].apply(lambda x: parse(x))        
        newCols = [f"c{i}_{c}" for i in range(3)]
        
        for ind, nc in enumerate(newCols):
            cells[nc] = cells[c].apply(lambda x: float(x[ind]))
        
    cells = cells.drop(INTEN_COLUMNS, axis=1)
    
    return cells


def mergeCellData(tracks, cells):
    """A function to merge track information with 
    cell information. Drops a few data intensive columns from
    cell data """
    
    # hand-picked columns
    CELL_COLUMNS = [
        'area', 
        'area_convex', 
        'area_filled', 
        'axis_major_length',
        'axis_minor_length', 
        'centroid_y', 
        'centroid_x', 
        'eccentricity',
        'c0_intensity_max', 
        'c1_intensity_max',
        'c2_intensity_max', 
        'c0_intensity_min',
        'c1_intensity_min',
        'c2_intensity_min', 
        'c0_intensity_mean',
        'c1_intensity_mean',
        'c2_intensity_mean',
        'label',
        'orientation', 
        'perimeter',
        'solidity', 
        'circularity',
        't'
    ]    
    
    # prepare for merging 
    cells = cells[CELL_COLUMNS]
    cells = cells.rename(columns={'centroid_x' : 'x',
                                  'centroid_y' : 'y'})
    
    # force datatypes
    mergeCols = {
        'x' : float,
        'y' : float,
        't' : int,
    }
    
    for k, v in mergeCols.items():
        cells[k] = cells[k].astype(v)
        tracks[k] = tracks[k].astype(v)
    
    # merge with tracks based on position and time
    tracks = pd.merge(tracks, cells, 
                      how='left',
                      left_on=list(mergeCols.keys()),
                      right_on=list(mergeCols.keys()),)
    
    return tracks


def renameCols(columns):
    """utility function to rename pivotted columns"""
    newColumns = []
    for c in columns:
        if c[1] != "":
            newColumns.append(f"c{c[1]}_{c[0]}_{c[2]}")
        else:
            newColumns.append(c[0])
    return newColumns


def reformatScores(scores):
    """a function to pivot scores """
    scores = pd.pivot_table(scores, 
                            values=['pval', 'logFoldChange'], 
                            index=['t', 'label'], 
                            columns=['c', 'name']).reset_index(drop=False)

    scores.columns = scores.columns.to_flat_index()
    scores.columns = renameCols(scores.columns)
    return scores
    
    
def mergeScores(tracks, scores):
    """a function to merge scores"""
    tracks['label']
    
    tracks['label'] = tracks['label'].astype('Int64')
    scores['label'] = scores['label'].astype('Int64')
    
    tracks['t'] = tracks['t'].astype('Int64')
    scores['t'] = scores['t'].astype('Int64')
    
    tracks = pd.merge(tracks, scores, 
                      how='left',
                      left_on=['t', 'label'],
                      right_on=['t', 'label'],)
    return tracks

    


if __name__ == "__main__":
    outpath = sys.argv[1]
    
    # load the data frames
    tracks = pd.read_csv(sys.argv[2])
    cells = pd.read_csv(sys.argv[3])
    scores = pd.read_csv(sys.argv[4])
    
    print(f"{tracks.shape=}")
    print(f"{cells.shape=}")
    print(f"{scores.shape=}")
    
    # reformat cells
    cells = splitIntensityStats(cells)
    
    # merge cell data
    tracks = mergeCellData(tracks, cells)
    tracks = tracks.sort_values(by=['t', 'label'])
    
    # reformat scores data
    scores = reformatScores(scores)
    
    # merge scores:
    tracks = mergeScores(tracks, scores)
    
    # sort and save
    tracks = tracks.sort_values(by=['t', 'label'])
    
    tracks.to_csv(outpath, index=False)
    
    
    
    
    
    
    
    
    
    