#!/usr/bin/env python3
import os
import glob
import argparse
import sys


def build_encoding_cmd(video, height, crf, outputfolder):

    settings = {
        "height": height,
        "crf": crf,
    }
    outputfile = outputfolder + "/" + os.path.splitext(os.path.basename(video))[0] + "_"
    outputfile += "crf_{}_".format(str(settings["crf"]).zfill(2))
    outputfile += "height_{}".format(str(settings["height"]).zfill(4))

    settings["video"] = video
    settings["outputfile"] = outputfile

    cmd = """
    ffmpeg -y -i "{video}" -vf scale=-2:{height} \
        -timecode_frame_start 1 -vframes 1 \
        -c:v libx265 -crf {crf} -c:a aac -strict -2 "{outputfile}.mkv" &&
    ffmpeg -y -i "{outputfile}.mkv"  \
        -timecode_frame_start 1 -vframes 1 \
        -f image2 "{outputfile}.png"
    """.format(**settings)

    cmd = " ".join(cmd.split())
    return cmd


def main(_):
    # argument parsing
    parser = argparse.ArgumentParser(description='create encoding commands for 1 frame analysis',
                                     epilog="stg7 2018",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("video", type=str, nargs="+", help="input video, a center cropped 1 frame video")
    parser.add_argument("--output", type=str, default="encoded", help="folder for storing the encoded videos")
    parser.add_argument("--cmd_file", type=str, default="encode_commands.list", help="file where all encoding commands are stored")

    a = vars(parser.parse_args())
    outputfolder = a["output"]

    os.makedirs(outputfolder, exist_ok=True)

    cmds = []
    for video in a["video"]:
        print(video)
        bname = os.path.basename(os.path.splitext(video)[0]).split(".")[0]
        output = outputfolder + "/" + bname
        os.makedirs(output, exist_ok=True)
        for height in range(144, 2161, 16):
            for crf in range(0, 51):
                cmds.append(build_encoding_cmd(video, height, crf, output))
    with open(a["cmd_file"], "w") as cfile:
        cfile.write("\n".join(cmds))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

