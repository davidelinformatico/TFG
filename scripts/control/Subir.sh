echo "Tiramos todos los Gpio"

gpio -g mode 17 in
gpio -g mode 4 in
gpio -g mode 27 in
gpio -g mode 22 in
gpio -g mode 5 in
gpio -g mode 6 in
gpio -g mode 13 in
gpio -g mode 19 in
gpio -g mode 23 in
gpio -g mode 24 in

echo "Todos los Gpio tirados"


echo "Subimos la persiana la persiana de las Maquinas"

sleep 1

gpio -g mode 19 out

sleep 15

gpio -g mode 19 in



echo "Subimos la persiana la persiana del Dormitorio"

gpio -g mode 17 out

sleep 5

gpio -g mode 17 in



echo "Subimos la persiana la persiana de la Cocina"

gpio -g mode 23 out

sleep 14

gpio -g mode 23 in



echo "Subimos la persiana la persiana del Comedor"

gpio -g mode 27 out

sleep 15

gpio -g mode 27 in



echo "Subimos la persiana la persiana del Despacho"

gpio -g mode 5 out

sleep 15

gpio -g mode 5 in



gpio -g mode 17 in
gpio -g mode 4 in
gpio -g mode 27 in
gpio -g mode 22 in
gpio -g mode 5 in
gpio -g mode 6 in
gpio -g mode 13 in
gpio -g mode 19 in
gpio -g mode 23 in
gpio -g mode 24 in



