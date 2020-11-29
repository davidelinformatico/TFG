echo "Tiramos todos los Gpio"

gpio -g mode 16 in
gpio -g mode 20 in
gpio -g mode 21 in
gpio -g mode 7 in
gpio -g mode 8 in

echo "Encendemos la luz de las Máquinas"
gpio -g mode 16 out
sleep 15

echo "Encendemos la luz del Dormitorio"
gpio -g mode 20 out
sleep 15

echo "Encendemos la luz de la Cocina"
gpio -g mode 21 out
sleep 15

echo "Encendemos la luz del Comedor"
gpio -g mode 7 out
sleep 15

echo "Encendemos la luz del Despacho"
gpio -g mode 8 out

gpio -g mode 16 in
gpio -g mode 20 in
gpio -g mode 21 in
gpio -g mode 7 in
gpio -g mode 8 in





