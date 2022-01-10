#!/usr/bin/env python3
import glob
import os

cmd = """./vmaf.py --pixel_format yuv422p10le --height 2160 --width 2160 --report_folder ./reports/{bn} {src} {dis} """

commands = []
for x in glob.glob("src_cropped/*"):
    if not os.path.isfile(x):
        continue
    print(x)
    bn = os.path.basename(x).split(".")[0]
    encoded_path = "encoded/" + bn
    for y in glob.glob(encoded_path + "/*.mkv"):

        xcmd = cmd.format(src=x, dis=y, bn=bn)
        commands.append(xcmd)

with open("vmaf_cmds.list", "w") as vfp:
    vfp.write("\n".join(commands))