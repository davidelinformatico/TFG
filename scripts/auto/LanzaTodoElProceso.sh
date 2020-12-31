#!/bin/bash
path=$(pwd)
echo $path
echo "${path/*}"

# Este script se ha desarrollado para lanzar todo el proceso desde CRON.
python3 ${path%/*}/auto/1_recabaInfo.py
python3 ${path%/*}/auto/3_cocinado.py
sh ${path%/*}/auto/4_reescribeCron.sh
