rule plotBackground:
    input:
        OUTPUT + "background/{iid}.{stage}.background.csv",
    output:
        OUTPUT + "plots/{iid}.{stage}.background.png"
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(imageIds)]),
        stage='prepared|processed'
    params:
        config=str(BASE_DIR) + "/config/config.yaml",
    shell:
        "python scripts/plotBackground.py {input} {params.config} {output}"