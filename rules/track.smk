rule track:
    input:
        btrack=config['btrack']['path'],
        img=OUTPUT + "images/{iid}.processed.tiff",
        seg=OUTPUT + "images/{iid}.segmented.tiff",
    output:
        OUTPUT + "tracks/{iid}.tracks.raw.csv",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(imageIds)]),
    params:
        tconf=config['btrack']['config'],
    shell:
        "python scripts/track.py {input.btrack} {input.img} {input.seg} {params.tconf} {output}"
        
        
rule mergeTrackData:
    input:
        tracks=OUTPUT + "tracks/{iid}.tracks.raw.csv",
        cells=OUTPUT + "segmentation/{iid}.celldata.csv",
        scores=OUTPUT + "segmentation/{iid}.intensity_scores.csv",
    output:
        OUTPUT + "tracks/{iid}.tracks.full.csv",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(imageIds)]),
    shell:
        "python scripts/mergeTrackInfo.py {output} {input}"
        