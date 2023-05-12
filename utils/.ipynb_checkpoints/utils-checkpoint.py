import pandas as pd
import os
import sys
from tifffile import imread
from tifffile import TiffFile


def getImages(path):
    """A function to import basecalls """
    imageDf = pd.read_csv(path,  comment="#")
    return imageDf


# def getImageOutputPath(imageDf, outputDir):
#     """A function to import basecalls """
#     outputFiles = []
#     for idx, row in imageDf.iterrows():
#         imgPath = row['filePath']
#         imgId = row['imageId']
        
#         with TiffFile(imgPath) as tif:
#             series = tif.series[0]
            
#         nTimePoints = series.shape[1]
#         for t in range(1, nTimePoints+1):
#             outputName = f"{outputDir}images/{imgId}_{t}.tiff"
#             outputFiles.append(outputName)
#     return outputFiles


def getImageMetadataPath(imageDf, outputDir):
    """A function to import basecalls """
    outputFiles = []
    for idx, row in imageDf.iterrows():
        imId = row['imageId']
        outputName = f"{outputDir}metadata/{imId}.json"
        outputFiles.append(outputName)
    return outputFiles


def expandImageIds(imageDf):
    """A function to return snakemake `expand` inputs """
    iids = []
    tids = []
    for idx, row in imageDf.iterrows():
        
        imgPath = row['FilePath']
        imgId = row['imageId']

        with TiffFile(imgPath) as tif:
            series = tif.series[0]
            
        nTimePoints = series.shape[1]
        for t in range(nTimePoints):
            iids.append(imgId)
            tids.append(t)
            
    return iids, tids


