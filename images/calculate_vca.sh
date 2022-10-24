#!/bin/bash
bn=$(basename $1)
echo "$(basename $1)"
ffmpeg -i "$1" -strict -1 -f yuv4mpegpipe - | ./VCA/build/source/apps/vca/vca --y4m --input stdin --complexity-csv vca.csv --videofilename "$bn"
