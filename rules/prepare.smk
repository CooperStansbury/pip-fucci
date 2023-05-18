rule getRawImages:
    input:
        imgs=imageDf['FilePath'].to_list()
    output:
        expand(f"{OUTPUT}images/{{iid}}.raw.tiff", iid=imageIds)
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(imageIds)]),
    run:
        from shutil import copyfile
        for i, imgPath in enumerate(input.imgs):
            outPath = output[i]
            copyfile(imgPath, outPath)


rule getMetaData:
    input:
        OUTPUT + "images/{iid}.raw.tiff"
    output:
        OUTPUT + "metadata/{iid}.metadata.json"
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(imageIds)]),
    shell:
        "python scripts/getMetadata.py {input} {output}"
        

rule prepareImage:
    input:
        img=OUTPUT + "images/{iid}.raw.tiff",
    output:
        OUTPUT + "images/{iid}.prepared.tiff"
    params:
        config=str(BASE_DIR) + "/config/config.yaml"
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(imageIds)]),
    shell:
        "python scripts/prepareImage.py {input.img} {params.config} {output}"

    
# prepare images for segmentation
rule preprocessImage:
    input:
        img=OUTPUT + "images/{iid}.prepared.tiff",
    output:
        OUTPUT + "images/{iid}.processed.tiff"
    params:
        config=str(BASE_DIR) + "/config/config.yaml"
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(imageIds)]),
    shell:
        "python scripts/processImage.py {input.img} {params.config} {output}"
