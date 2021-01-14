#!/bin/bash
##############################################################################
### Este script se ha desarrollado para lanzar todo el proceso desde CRON. ###
##############################################################################

python3 ${PWD%/*}/auto/1_recabaInfo.py
python3 ${PWD%/*}/auto/3_cocinado.py
sh ${PWD%/*}/auto/4_reescribeCron.sh
