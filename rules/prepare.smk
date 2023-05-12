# extract the metadata 
rule getMetaData:
    input:
        imageDf['FilePath'].to_list()
    output:
        utils.getImageMetadataPath(imageDf, OUTPUT)
    shell:
        "python scripts/getMetadata.py {input} {output}"
        
# load images and split on time pionts 
# so each has an independant job
rule getImages:
    input:
        imgs=imageDf['FilePath'].to_list(),
        config=str(BASE_DIR) + "/config/config.yaml"
    output:
        temp(expand(f"{OUTPUT}images/{{imgId}}_{{tid}}.raw.tiff", zip, imgId=iids, tid=tids))
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(iids)]),
        tid='|'.join([re.escape(str(x)) for x in set(tids)]),
    shell:
        "python scripts/loadImg.py {input.imgs} {input.config} {output}"
        
        
# prepare images for segmentation
rule preprocess:
    input:
        img=OUTPUT + "images/{iid}_{tid}.raw.tiff",
        config=str(BASE_DIR) + "/config/config.yaml",
    output:
        imgs=temp(OUTPUT + "images/{iid}_{tid}.processed.tiff"),
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(iids)]),
        tid='|'.join([re.escape(str(x)) for x in set(tids)]),
    shell:
        "python scripts/preprocess.py {input.img} {input.config} {output.imgs}"
        

# gather split files into single, sorted tiffs 
rule mergeRaw:
    input:        
        imgs=expand(f"{OUTPUT}images/{{imgId}}_{{tid}}.raw.tiff", zip, imgId=iids, tid=tids),
    output:
        OUTPUT + "images/{iid}.raw.tiff"
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(iids)]),
        tid='|'.join([re.escape(str(x)) for x in set(tids)]),
    shell:
        "python scripts/mergeTiff.py {output} {input}"
        
        
rule mergeProcessed:
    input:        
        imgs=expand(f"{OUTPUT}images/{{imgId}}_{{tid}}.processed.tiff", zip, imgId=iids, tid=tids),
    output:
        OUTPUT + "images/{iid}.processed.tiff"
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(iids)]),
        tid='|'.join([re.escape(str(x)) for x in set(tids)]),
    shell:
        "python scripts/mergeTiff.py {output} {input}"
        
        