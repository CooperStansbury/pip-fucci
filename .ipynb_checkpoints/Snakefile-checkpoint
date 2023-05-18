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
imageIds = imageDf['imageId'].unique()


# global vars
STAGES = ['prepared', 'processed']


################ RULE FILES ################
include: "rules/prepare.smk"
include: "rules/segment.smk"
include: "rules/track.smk"
include: "rules/plots.smk"


rule all:
    input:
        expand(f"{OUTPUT}images/{{imgId}}.raw.tiff", imgId=imageIds),
        expand(f"{OUTPUT}images/{{imgId}}.prepared.tiff", imgId=imageIds),
        expand(f"{OUTPUT}images/{{imgId}}.processed.tiff", imgId=imageIds),
        expand(f"{OUTPUT}metadata/{{imgId}}.metadata.json", imgId=imageIds),
        expand(f"{OUTPUT}images/{{imgId}}.segmented.tiff", imgId=set(imageIds)),
        expand(f"{OUTPUT}segmentation/{{imgId}}.intensities.csv", imgId=set(imageIds)),
        expand(f"{OUTPUT}background/{{imgId}}.{{stage}}.background.csv", imgId=set(imageIds), stage=STAGES),
        expand(f"{OUTPUT}backgroundPlots/{{imgId}}.{{stage}}.png", imgId=set(imageIds), stage=STAGES),
        expand(f"{OUTPUT}segmentation/{{imgId}}.{{stage}}.scores.csv", imgId=set(imageIds), stage=STAGES),
        expand(f"{OUTPUT}movies/{{imgId}}.segmentation.gif", imgId=set(imageIds)),
        expand(f"{OUTPUT}tracks/{{imgId}}.tracks.raw.csv", imgId=set(imageIds)),
        # expand(f"{OUTPUT}tracks/{{imgId}}.tracks.full.csv", imgId=set(imageIds)),
        # expand(f"{OUTPUT}background/{{imgId}}.backgroundplot.png", imgId=set(imageIds)),
        # expand(f"{OUTPUT}background/{{imgId}}.masked.backgroundplot.png", imgId=set(imageIds)),
        # OUTPUT + "movies/test.segmented.tiff",
        

# rule cellCyclePredict:
#     input:
#         tracks=OUTPUT + "tracks/{iid}.tracks.full.csv",
#     output:
#         OUTPUT + "phase/{iid}.init.preds.csv",
#     shell:
#         "python scripts/predictPhase.py {input} {ouput}"
#         
#         
     