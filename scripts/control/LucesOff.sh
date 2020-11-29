gpio -g mode 16 in
gpio -g mode 20 in
gpio -g mode 21 in
gpio -g mode 7 in
gpio -g mode 8 in

echo "Apagamos la luz de las Máquinas"
gpio -g mode 16 in
sleep 15

echo "Apagamos la luz del Dormitorio"
gpio -g mode 20 in
sleep 15

echo "Apagamos la luz de la Cocina"
gpio -g mode 21 in
sleep 15

echo "Apagamos la luz del Comedor"
gpio -g mode 7 in
sleep 15

echo "Apagamos la luz del Despacho"
gpio -g mode 8 in

gpio -g mode 16 in
gpio -g mode 20 in
gpio -g mode 21 in
gpio -g mode 7 in
gpio -g mode 8 in