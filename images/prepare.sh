#!/bin/bash
git clone https://github.com/Netflix/vmaf.git
cd vmaf
git checkout 1b1d75db6bf44b62e9755121559c951c03199b2c

cd vmaf
cd ptools; make -j 12 ; cd ../wrapper; make -j 12 'CFLAGS=-Wall -O3 -mavx -mavx2'; cd ..;
