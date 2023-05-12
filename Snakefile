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


rule all:
    input:
        expand(f"{OUTPUT}metadata/{{imgId}}.json", imgId=set(iids)),
        expand(f"{OUTPUT}images/{{imgId}}.raw.tiff", imgId=set(iids)),
        expand(f"{OUTPUT}images/{{imgId}}.segmented.tiff", imgId=set(iids)),
        expand(f"{OUTPUT}images/{{imgId}}.processed.tiff", imgId=set(iids)),
        expand(f"{OUTPUT}segmentation/{{imgId}}.intensities.csv", imgId=set(iids)),
        expand(f"{OUTPUT}background/{{imgId}}.background.csv", imgId=set(iids)),
        expand(f"{OUTPUT}background/{{imgId}}.masked.background.csv", imgId=set(iids)),
        expand(f"{OUTPUT}segmentation/{{imgId}}.intensity_scores.csv", imgId=set(iids)),
        expand(f"{OUTPUT}tracks/{{imgId}}.tracks.raw.csv", imgId=set(iids)),
        expand(f"{OUTPUT}tracks/{{imgId}}.tracks.full.csv", imgId=set(iids)),
        
        
rule track:
    input:
        btrack=config['btrack']['path'],
        img=OUTPUT + "images/{iid}.processed.tiff",
        seg=OUTPUT + "images/{iid}.segmented.tiff",
        tconf=config['btrack']['config'],
    output:
        OUTPUT + "tracks/{iid}.tracks.raw.csv",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(iids)]),
    shell:
        "python scripts/track.py {input.btrack} {input.img} {input.seg} {input.tconf} {output}"
        
        
rule mergeTrackData:
    input:
        tracks=OUTPUT + "tracks/{iid}.tracks.raw.csv",
        cells=OUTPUT + "segmentation/{iid}.celldata.csv",
        scores=OUTPUT + "segmentation/{iid}.intensity_scores.csv",
    output:
        OUTPUT + "tracks/{iid}.tracks.full.csv",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(iids)]),
    shell:
        "python scripts/mergeTrackInfo.py {output} {input}"
        