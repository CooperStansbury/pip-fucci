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
        presc=OUTPUT + "segmentation/{iid}.prepared.scores.csv",
        procsc=OUTPUT + "segmentation/{iid}.processed.scores.csv",
    output:
        OUTPUT + "tracks/{iid}.tracks.full.csv",
    wildcard_constraints:
        iid='|'.join([re.escape(x) for x in set(imageIds)]),
    shell:
        "python scripts/mergeTrackData.py {input.tracks} {input.cells} {input.presc} {input.procsc} {output}"
        