#!/usr/bin/env python3
import os
import sys
import shutil
import json
import argparse
import logging
import subprocess


VMAF_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./vmaf/wrapper/vmafossexec"))
VMAF_MODEL = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./vmaf/model/vmaf_4k_rb_v0.6.2/vmaf_4k_rb_v0.6.2.pkl"))


def assert_file(filename, error_msg):
    if not os.path.isfile(filename):
        logging.error("you need to have a compiled vmaf running, so run ./prepare.sh and check errors")
        raise Exception()


def shell_call(call):
    """
    Run a program via system call and return stdout + stderr.
    @param call programm and command line parameter list, e.g ["ls", "/"]
    @return stdout and stderr of programm call
    """
    try:
        output = subprocess.check_output(call, universal_newlines=True, shell=True)
    except Exception as e:
        output = str(e.output)
    return output


def ffprobe(filename):
    """ run ffprobe to get some information of a given video file
    """
    if shutil.which("ffprobe") is None:
        raise Exception("you need to have ffprobe installed, please read README.md.")

    if not os.path.isfile(filename):
        raise Exception("{} is not a valid file".format(filename))

    cmd = "ffprobe -show_format -select_streams v:0 -show_streams -of json {filename} 2>/dev/null".format(filename=filename)

    res = shell_call(cmd).strip()

    if len(res) == 0:
        raise Exception("{} is somehow not valid, so ffprobe could not extract anything".format(filename))

    res = json.loads(res)

    needed = {"pix_fmt": "unknown",
              "bits_per_raw_sample": "unknown",
              "width": "unknown",
              "height": "unknown",
              "avg_frame_rate": "unknown",
              "codec_name": "unknown"
             }
    for stream in res["streams"]:
        for n in needed:
            if n in stream:
                needed[n] = stream[n]
                if n == "avg_frame_rate":  # convert framerate to numeric integer value
                    needed[n] = round(eval(needed[n]))
    needed["bitrate"] = res.get("format", {}).get("bit_rate", -1)
    needed["codec"] = needed["codec_name"]

    return needed


def get_basename(filename):
    return os.path.splitext(filename)[0]


def flat_name(filename):
    return filename.replace("../", "").replace("/", "_")


def to_yuv(src, yuv_result, pixel_format, height, width, framerate):
    if os.path.isfile(yuv_result):
        logging.info("{} already converted".format(yuv_result))
        return
    logging.info(f"convert {src} to {yuv_result}")
    cmd = " ".join(f"""
    ffmpeg -y -i "{src}"
        -vf scale={width}:{height},fps={framerate}
        -c:v rawvideo
        -framerate {framerate}
        -pix_fmt {pixel_format} "{yuv_result}"
    """.split())
    os.system(cmd)


def run_vmaf(ref, dis, tmp_folder_ref, tmp_folder_dis, report_folder, pixel_format="yuv422p10le", height=2160, width=3840, framerate=60, vmaf_model="vmaf_4k_v0.6.1.pkl", delete_yuv_ref=False):
    os.makedirs(tmp_folder_ref, exist_ok=True)
    os.makedirs(tmp_folder_dis, exist_ok=True)
    os.makedirs(report_folder, exist_ok=True)

    yuv_ref = os.path.join(tmp_folder_ref, flat_name(get_basename(ref)) + ".yuv")
    yuv_dis = os.path.join(tmp_folder_dis, flat_name(get_basename(dis)) + ".yuv")

    report_name = os.path.join(report_folder, flat_name(get_basename(dis)) + ".json")

    if os.path.isfile(report_name):
        logging.info("{} already calculated".format(report_name))
        return
    logging.info(f"convert to yuv {ref}, {dis}")
    to_yuv(ref, yuv_ref, pixel_format, height, width, framerate)
    to_yuv(dis, yuv_dis, pixel_format, height, width, framerate)

    logging.info(f"calculate vamf {ref}, {dis}")


    vmaf_cmd = f"""
    {VMAF_PATH} {pixel_format} {width} {height} {yuv_ref} {yuv_dis} {VMAF_MODEL} --log {report_name} --log-fmt json --thread 0 --psnr --ssim --ms-ssim --ci
    """.strip()
    os.system(vmaf_cmd)
    # only delete distorted video yuv file, however reference video is maybe used somewhere else
    os.remove(yuv_dis)
    if delete_yuv_ref:
        os.remove(yuv_ref)

    logging.info(f"vmaf calculation done for {ref}, {dis}")
    return report_name



def main(_):
    # argument parsing
    parser = argparse.ArgumentParser(description='run vmaf calculation, with yuv conversion',
                                     epilog="stg7 2018",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("reference_video", type=str, help="reference video")
    parser.add_argument("distorted_video", type=str, help="distorted video")
    parser.add_argument("--tmp_folder_ref", type=str, default="./yuv_r", help="tmp folder for storing converted reference videos")
    parser.add_argument("--tmp_folder_dis", type=str, default="./yuv_d", help="tmp folder for storing converted distorted videos")
    parser.add_argument("--report_folder", type=str, default="./reports", help="folder for storing reports")
    parser.add_argument("--pixel_format", type=str, default="yuv422p10le", help="pixel_format")
    parser.add_argument("--height", type=int, default=2160, help="height")
    parser.add_argument("--width", type=int, default=3840, help="width")
    parser.add_argument("--framerate", type=int, default=60, help="framerate")
    parser.add_argument("--meta_from_ref", action='store_true', help="estimate framerate, height, width, pixel_format from reference video")
    parser.add_argument("--vmaf_model", type=str, default=VMAF_MODEL, help="used VMAF model")

    logging.basicConfig(level=logging.DEBUG)
    logging.info("calculate vmaf scores")

    a = vars(parser.parse_args())
    logging.info("params: {}".format(a))
    print(VMAF_PATH)

    assert_file(VMAF_PATH, "you need to have a compiled vmaf running, so run ./prepare.sh and check errors")
    assert_file(a["reference_video"], f"""reference video {a["reference_video"]} does not exist""")
    assert_file(a["distorted_video"], f"""distorted video {a["distorted_video"]} does not exist""")

    if a["meta_from_ref"]:
        meta = ffprobe(a["reference_video"])
        logging.info(f"estimated meta data: \n {json.dumps(meta, indent=4, sort_keys=True)}")
        a["height"] = meta["height"]
        a["framerate"] = meta["avg_frame_rate"]
        a["pixel_format"] = meta["pix_fmt"]

    run_vmaf(
        a["reference_video"],
        a["distorted_video"],
        a["tmp_folder_ref"],
        a["tmp_folder_dis"],
        a["report_folder"],
        a["pixel_format"],
        a["height"],
        a["width"],
        a["framerate"],
        a["vmaf_model"]
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
