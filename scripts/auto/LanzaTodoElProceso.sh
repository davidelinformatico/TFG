#!/bin/bash
path=$(pwd)
echo $path
echo "${path%/*}"

python3 ${path%/*}/auto/Generahoras.py
python3 ${path%/*}/auto/RecogeHoras.py
sh ${path%/*}/auto/reescribeCron.sh