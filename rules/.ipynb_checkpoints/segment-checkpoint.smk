# segment each cell    
rule segment:
    input:
        img=OUTPUT + "images/{iid}.processed.tiff",
    output:
        seg=OUTPUT + "images/{iid}.segmented.tiff",
        data=OUTPUT + "segmentation/{iid}.celldata.csv",
        inten=OUTPUT + "segmentation/{iid}.intensities.csv",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(imageIds)]),
    params:
        config=str(BASE_DIR) + "/config/config.yaml",
    shell:
        "python scripts/segment.py {input.img} {params.config} {output.seg} {output.data} {output.inten}"


rule getBackground:
    input:
        OUTPUT + "images/{iid}.{stage}.tiff", 
    output:
        OUTPUT + "background/{iid}.{stage}.background.csv",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(imageIds)]),
        stage='prepared|processed'
    shell:
        "python scripts/getBackground.py {input} {output}"


rule scoreIntensities:
    input:
        img=OUTPUT + "segmentation/{iid}.intensities.csv",
        bk=OUTPUT + "background/{iid}.{stage}.background.csv",
    output:
        OUTPUT + "segmentation/{iid}.{stage}.scores.csv",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(imageIds)]),
        stage='prepared|processed'
    shell:
        "python scripts/scoreIntensity.py {input.img} {input.bk} {output}"


rule getSegmentationMovie:
    input:
        img=OUTPUT + "images/{iid}.processed.tiff",
        seg=OUTPUT + "images/{iid}.segmented.tiff",
    output:
        OUTPUT + "movies/{iid}.segmentation.gif",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(imageIds)]),
    params:
        config=str(BASE_DIR) + "/config/config.yaml",
    shell:
        "python scripts/makeMovie.py {input.img} {input.seg} {params.config} {output}"