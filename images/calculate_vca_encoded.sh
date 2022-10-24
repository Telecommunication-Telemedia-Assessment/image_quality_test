#!/bin/bash

find /home/sgoering/shares/avt_80tb/co_worker/steve/one_frame_vmaf_perception_differences/encoded/ -name "*.mkv" | xargs -i -P 200 ./calculate_vca.sh {} | grep "{\"video" >  vca_encoded.ldjson