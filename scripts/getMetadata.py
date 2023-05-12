import sys
import pandas as pd
import numpy as np
from pathlib import Path
from tifffile import tiffcomment
import xmltodict
import json






if __name__ == "__main__":
    imgPath = sys.argv[1]  
    outpath = sys.argv[2]  
    
    rawMeta = tiffcomment(imgPath)
    metaDict = xmltodict.parse(rawMeta)
    
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(metaDict, f, ensure_ascii=False, indent=4)
    

    