rule plotBackgroundRaw:
    input:
        inten=OUTPUT + "background/{iid}.background.raw.csv",
        config=str(BASE_DIR) + "/config/config.yaml",
    output:
        OUTPUT + "background/{iid}.raw.backgroundplot.png",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(iids)]),
    shell:
        "python scripts/plotBackground.py {input.inten} {input.config} {output}"
        
        
rule plotBackground:
    input:
        inten=OUTPUT + "background/{iid}.background.csv",
        config=str(BASE_DIR) + "/config/config.yaml",
    output:
        OUTPUT + "background/{iid}.backgroundplot.png",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(iids)]),
    shell:
        "python scripts/plotBackground.py {input.inten} {input.config} {output}"
        
        
rule plotBackgroundMasked:
    input:
        inten=OUTPUT + "background/{iid}.masked.background.csv",
        config=str(BASE_DIR) + "/config/config.yaml",
    output:
        OUTPUT + "background/{iid}.masked.backgroundplot.png",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(iids)]),
    shell:
        "python scripts/plotBackground.py {input.inten} {input.config} {output}"