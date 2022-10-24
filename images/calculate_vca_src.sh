#!/bin/bash
find src_cropped -name "*.mkv" | xargs -i -P 20 ./calculate_vca.sh {} | grep "{\"video" >  vca_scr.ldjson