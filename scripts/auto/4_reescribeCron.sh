#!/bin/bash
path=$(pwd)
echo $path
echo "${path/*}"


sudo cp $path/CronPruebas /var/spool/cron/crontabs/pi
sudo service cron restart
sudo service cron stop
sudo service cron start




#!/bin/bash
#path=$(pwd)
#echo $path
#echo "${path/*}"

# Este script se ha desarrollado para lanzar todo el proceso desde CRON.
#python3 ${path%/*}/auto/1_recabaInfo.py
#python3 ${path%/*}/auto/3_cocinado.py
#sh ${path%/*}/auto/4_reescribeCron.sh