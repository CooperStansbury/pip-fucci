# segment each cell    
rule segment:
    input:
        img=OUTPUT + "images/{iid}.processed.tiff",
        config=str(BASE_DIR) + "/config/config.yaml",
    output:
        seg=OUTPUT + "images/{iid}.segmented.tiff",
        data=OUTPUT + "segmentation/{iid}.celldata.csv",
        inten=OUTPUT + "segmentation/{iid}.intensities.csv",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(iids)]),
    shell:
        "python scripts/segment.py {input.img} {input.config} {output.seg} {output.data} {output.inten}"
        

rule getRawBackground:
    input:
        img=OUTPUT + "images/{iid}.raw.tiff", 
    output:
        OUTPUT + "background/{iid}.background.raw.csv",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(iids)]),
    shell:
        "python scripts/getBackground.py {input.img} {output}"


rule getBackground:
    input:
        img=OUTPUT + "images/{iid}.processed.tiff", 
    output:
        OUTPUT + "background/{iid}.background.csv",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(iids)]),
    shell:
        "python scripts/getBackground.py {input.img} {output}"
        
        
rule getMaskedBackground:
    input:
        img=OUTPUT + "images/{iid}.processed.tiff", 
        seg=OUTPUT + "images/{iid}.segmented.tiff",
    output:
        OUTPUT + "background/{iid}.masked.background.csv",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(iids)]),
    shell:
        "python scripts/getBackground.py {input.img} {input.seg} {output}"
        
        
rule score_intensities:
    input:
        OUTPUT + "segmentation/{iid}.intensities.csv",
        OUTPUT + "background/{iid}.background.csv",
        OUTPUT + "background/{iid}.masked.background.csv",
    output:
        OUTPUT + "segmentation/{iid}.intensity_scores.csv"
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(iids)]),    
    shell:
        'python scripts/scoreIntensity.py {output} {input}'