#!/bin/bash
find encoded/ -name "*.mkv" | xargs -i du -b {} > filesize.csv

