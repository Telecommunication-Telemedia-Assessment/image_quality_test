#!/usr/bin/env python3
import glob
import os
import json
import shutil

import pandas as pd
import numpy as np
import seaborn as sns

d = print

# using calculated vmaf score select the "best"/"optimal" files for each quality level (vmaf score)

base_frames = [os.path.basename(x) for x in glob.glob("reports/*")]
print(base_frames)
print(f"in total {len(base_frames)} frames slected/processed")

# read scores
values = []
for base_frame in base_frames:
    print(f"read {base_frame}")
    reports = list(glob.glob(f"reports/{base_frame}/*"))
    #print(reports[0:2])
    for r in reports:
        frame_name = os.path.basename(r).split(base_frame + "_", 1)[1].replace(".json", ".png")
        #print(frame_name)
        with open(r) as rfp:
            jr = json.load(rfp)
        vmaf = jr["frames"][0]["metrics"]["vmaf"]
        values.append({"vmaf": vmaf, "frame_name": frame_name, "base_frame": base_frame})
        #break
    #break


df = pd.DataFrame(values)
df["vmaf_round"] = df["vmaf"].round(0)
df["crf"] = df["frame_name"].apply(lambda x: int(x.split("crf_")[1].split("_")[0]))

df["height"] = df["frame_name"].apply(lambda x: int(x.split("height_")[1].split("_")[0].split(".")[0]))
d(df.head())


for baseframename, fg in df.groupby(by="base_frame"):
    selected = []
    print(f"handle {baseframename}")
    for x, g in fg.groupby(by="vmaf_round"):
        g = g[g["height"] <= g["height"].mean()]
        g = g[g["crf"] <= g["crf"].mean()]
        g = g[g["crf"] >= g["crf"].median()]
        g = g.sort_values(by="height")
        for _, r in g.iterrows():
            selected.append({
                "filename":r["frame_name"],
                "score": r["vmaf_round"]
            })
            break

    os.makedirs("playlist/" + baseframename, exist_ok=True)
    selection = pd.DataFrame(selected)
    selection.to_csv("playlist/" + baseframename + "/files.csv", index=False)
    for k, r in selection.iterrows():
        print(f"""copy {r["filename"]}""")
        filename = "encoded/" + baseframename + "/" + r["filename"]
        shutil.copy(filename, "playlist/" + baseframename + "/")
