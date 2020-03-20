# image quality test analysis and results

## general
all images were created based on repo `one_frame_vmaf_perception_differences`

for the test only a random selected subset was used:

* sampling was performed based on objective scores (vmaf)

* in `avrateNg.tar.lzma` the used avrate version is stored, to run the test you need to copy the image folder of this repo to the avrateNG folder.


## requirements
* python3, jupyter notebook

* for `extract_objective_metrics.ipynb` you need to extract `reports.tar.lzma` into this folder

## files

* `meta.csv`: summary of meta-data for image compression (considering only the images used in the test)
* `mos_ci.csv`: mos ci values extracted from the avrateNG ratings
* `per_user.csv`: per user ratings extracted from the avrateNG ratings
* `objective_metrics.csv`: results of objective metrics