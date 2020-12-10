echo "Ha comenzado el proceso de generación de ficheros"
python3 Generahoras.py
python3 RecogeHoras.py
sh reescribeCron.sh
echo "Ha finalizado el proceso de generación de ficheros"