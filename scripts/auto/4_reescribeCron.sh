#!/bin/bash
sudo cp ${PWD%/*}/auto/CronPruebas /var/spool/cron/crontabs/pi
sudo service cron restart
sudo service cron stop
sudo service cron start


