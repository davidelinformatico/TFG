#!/bin/sh
path=$(pwd)
echo $path

# Actualizamos todo el sistema
sudo apt-get update && sudo apt-get upgrade

# Actualizamos pip
python3.7 -m pip install --upgrade --force-reinstall pip

#Importamos para funcionamiento de Numpy
sudo apt-get install libatlas-base-dev

# Instalamos lo requerimientos
pip3 install --no-cache-dir -r requeriments

# Instalamos a mano pyTelegramBotAPI
python3.7 -m pip install --upgrade --force-reinstall pyTelegramBotAPI
python3.7 -m pip install --upgrade --force-reinstall python-telegram-bot

cp ${path%/*/*/*}/credentials/config2.bot ${path%}/config2.bot

# Lanzamos la generación de archivos
python3 ${path}/creator.py

rm config2.bot
rm requeriments
rm creator.py
rm $0
