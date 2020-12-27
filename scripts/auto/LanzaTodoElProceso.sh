#!/bin/bash
path=$(pwd)
echo $path

# Este script se ha desarrollado para lanzar todo el proceso desde CRON.
python3 ${path%}/1_recabaInfo.py
python3 ${path%}/3_cocinado.py
sh ${path%}/4_reescribeCron.sh