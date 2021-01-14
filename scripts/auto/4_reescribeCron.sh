#!/bin/bash
####################################################################
### Este archivo vuelca la configuración del archivo CronPruebas ###
### al archivo de configuración de Cron.						 ###
####################################################################

sudo cp ${PWD%/*}/auto/CronPruebas /var/spool/cron/crontabs/pi
sudo service cron restart
sudo service cron stop
sudo service cron start


