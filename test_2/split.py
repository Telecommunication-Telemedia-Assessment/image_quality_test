#!/usr/bin/env python3
import argparse
import sys
import os
import multiprocessing

import skimage.io

def img_show(x):
    skimage.io.imshow(x)
    skimage.io.show()


def img_split(img_filename, folder):
    os.makedirs(folder, exist_ok=True)
    img = skimage.io.imread(img_filename)

    h, w = img.shape[0:2]
    top_left = img[0:h // 2, 0:w // 2, ]
    top_right = img[0:h // 2, w // 2:, ]
    bottom_left = img[h // 2:, 0:w // 2, ]
    bottom_right = img[h // 2:, w // 2:, ]
    bn_img = os.path.join(
        folder,
        os.path.splitext(os.path.basename(img_filename))[0]
    )
    skimage.io.imsave(bn_img + "_tl.png", top_left, check_contrast=False)
    skimage.io.imsave(bn_img + "_tr.png", top_right, check_contrast=False)
    skimage.io.imsave(bn_img + "_bl.png", bottom_left, check_contrast=False)
    skimage.io.imsave(bn_img + "_br.png", bottom_right, check_contrast=False)
    #img_show(top_left)
    #img_show(top_right)
    #img_show(bottom_left)
    #img_show(bottom_right)
    print(f"{img_filename} done.")


def main(_):
    # argument parsing
    parser = argparse.ArgumentParser(description='split image into 4 patches',
                                     epilog="stg7 2020",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("image", type=str, nargs="+", help="image to be splitted")
    parser.add_argument("--output_folder", type=str, default="splits", help="folder to store all splitted images")
    parser.add_argument('--cpu_count', type=int, default=multiprocessing.cpu_count() // 2, help='thread/cpu count')

    a = vars(parser.parse_args())

    pool = multiprocessing.Pool(processes=a["cpu_count"])

    params = [(image, a["output_folder"]) for image in a["image"]]
    pool.starmap(img_split, params)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))


