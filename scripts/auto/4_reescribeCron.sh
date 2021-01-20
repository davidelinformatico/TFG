#!/bin/bash
####################################################################
### Este archivo vuelca la configuración del archivo CronPruebas ###
### al archivo de configuración de Cron. En caso de no tener las ###
### líneas esperadas en CronPruebas no se vuelca el contenido,   ###
### dejando constancia en el archivo erroresCronPruebas.         ###
####################################################################


lineas=`cat ${PWD%/*}/auto/CronPruebas | wc -l`

if [ $lineas = 82 ];
then
    sudo cp ${PWD%/*}/auto/CronPruebas /var/spool/cron/crontabs/pi
    sudo service cron restart
    sudo service cron stop
    sudo service cron start
else
    DIA=`date +"%d/%m/%Y"`
    HORA=`date +"%H:%M"`

    sed -i '1i Error CronPruebas - $DIA $HORA' erroresCronPruebas.txt
fi



