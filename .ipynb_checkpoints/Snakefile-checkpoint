import pandas as pd
import yaml
from pathlib import Path
import re
import os
import sys
from utils import utils
from snakemake.utils import Paramspace

BASE_DIR = Path(workflow.basedir)
configfile: str(BASE_DIR) + "/config/config.yaml"

# structure file names and get Id lists
OUTPUT = config['output_path']
imagePath = os.path.abspath(config['images'])
imageDf = utils.getImages(imagePath)
iids, tids = utils.expandImageIds(imageDf)

################ RULE FILES ################
include: "rules/prepare.smk"
include: "rules/segment.smk"
include: "rules/track.smk"
include: "rules/plots.smk"


rule all:
    input:
        expand(f"{OUTPUT}metadata/{{imgId}}.json", imgId=set(iids)),
        expand(f"{OUTPUT}images/{{imgId}}.raw.tiff", imgId=set(iids)),
        expand(f"{OUTPUT}images/{{imgId}}.segmented.tiff", imgId=set(iids)),
        expand(f"{OUTPUT}images/{{imgId}}.processed.tiff", imgId=set(iids)),
        expand(f"{OUTPUT}segmentation/{{imgId}}.intensities.csv", imgId=set(iids)),
        expand(f"{OUTPUT}background/{{imgId}}.background.csv", imgId=set(iids)),
        expand(f"{OUTPUT}background/{{imgId}}.background.raw.csv", imgId=set(iids)),
        expand(f"{OUTPUT}background/{{imgId}}.masked.background.csv", imgId=set(iids)),
        expand(f"{OUTPUT}segmentation/{{imgId}}.intensity_scores.csv", imgId=set(iids)),
        expand(f"{OUTPUT}tracks/{{imgId}}.tracks.raw.csv", imgId=set(iids)),
        expand(f"{OUTPUT}tracks/{{imgId}}.tracks.full.csv", imgId=set(iids)),
        expand(f"{OUTPUT}background/{{imgId}}.raw.backgroundplot.png", imgId=set(iids)),
        expand(f"{OUTPUT}background/{{imgId}}.backgroundplot.png", imgId=set(iids)),
        expand(f"{OUTPUT}background/{{imgId}}.masked.backgroundplot.png", imgId=set(iids)),
        


def makeSegmentationMovie:
    input:
        img=OUTPUT + "images/{iid}.processed.tiff",
        seg=OUTPUT + "images/{iid}.segmented.tiff",
    output:
        OUTPUT + "movies/{iid}.segmented.tiff",
    shell:

# 
# rule cellCyclePredict:
#     input:
#         tracks=OUTPUT + "tracks/{iid}.tracks.full.csv",
#     output:
#         OUTPUT + "phase/{iid}.init.preds.csv",
#     shell:
#         "python scripts/predictPhase.py {input} {ouput}"
#         
#         
     