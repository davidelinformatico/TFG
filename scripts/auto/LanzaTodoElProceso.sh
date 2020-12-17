#!/bin/bash
path=$(pwd)
echo $path
echo "${path%/*}"

python3 ${path%/*}/auto/1_SistemaAutomatico.py
python3 ${path%/*}/auto/2_SistemaTemperatura.py
sh ${path%/*}/auto/reescribeCron.sh