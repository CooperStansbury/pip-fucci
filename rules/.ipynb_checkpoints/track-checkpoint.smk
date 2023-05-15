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
        