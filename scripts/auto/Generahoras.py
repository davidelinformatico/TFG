#!/usr/bin/env python3
import urllib, json, datetime, pycurl, requests, os 
import datetime, time
import pandas as pd 
import matplotlib.pyplot as plt

#Calculamos ruta
ruta=os.getcwd().split('/')
rutaPrincipal=os.getcwd().split('/')
salida=""
for i in range(len(ruta)-3):
    salida=str(salida)+"/"+str(ruta[i])
ruta=salida[1:]+str("/credentials")

cosa=""
for i in range(len(rutaPrincipal)-1):
    cosa=str(cosa)+"/"+str(rutaPrincipal[i])
rutaPrincipal=cosa[1:]+str("/auto/")
#print("Ha comenzado el proceso de cálculo de horas.")

# Obtención de los seriales

# Llamamos a mi key personal de Climacell, que está en otro directorio.
result = open(ruta+'/KeyClimacell')
KeyClimacell = result.read()
result.close() 
# Llamamos a mi key personal de Climacell, que está en otro directorio.
result = open(ruta+'/KeyWeatherapi')
KeyWeatherapi = result.read()
result.close() 
id_weatherapi = KeyWeatherapi 


# Hora más temprana de subida de persianas (configurable desde el bot)
HoraMinima=rutaPrincipal+"HoraMinima"
f = open(HoraMinima)
hora_minima = f.read()
f.close()

#Leemos la cabecera del futuro archivo CRON, se puede obtener mediante 'cat' pero prefiero tener copia de seguridad.
c = open (rutaPrincipal+'cabecera.txt')
cabecera = c.read()
c.close()

#Ip's que vamos a utilizar
url_ip="http://ip-api.com/json/?fields=city,query,regionName"
url_tiempo = "https://api.climacell.co/v3/weather/forecast/hourly"

#Obtenemos fecha de hoy y de mañana
ahora = time.ctime(time.time())
hoy=datetime.date.today()
fecha_manana = hoy + datetime.timedelta(1)

# Geolocalización
sopa = requests.get(url_ip)
prueba = sopa.json()
ciudad = prueba['city']
ip_publica = prueba['query']
region = prueba['regionName']

#Tiempo mañana en la ubicación de la máquina
url_tiempo = "http://api.weatherapi.com/v1/astronomy.json?key="+str(id_weatherapi)+"&q="+ciudad+"&dt="+str(fecha_manana)+""
resp = requests.get(url_tiempo)
diccionario = resp.json()
loc = diccionario['astronomy']
ast = loc['astro']

#Hora en que amanece y anochece en formato 24h
amanece = pd.to_datetime(ast['sunrise']).strftime('%H:%M:%S')
anochece = pd.to_datetime(ast['sunset']).strftime('%H:%M:%S')
enlaza = str(hoy)+" "+str(anochece)
media_hora =str(hoy)+" "+str('00:30:00')


# Generamos las horas finales para incluirlas en el script
from datetime import datetime # Esto es necesario aquí
datetime_Bajada_Buena = datetime.strptime(enlaza, "%Y-%m-%d %H:%M:%S")
import datetime # Esto es necesario aquí
real_On = datetime_Bajada_Buena + datetime.timedelta(minutes=10)
real_down_1 = datetime_Bajada_Buena + datetime.timedelta(minutes=15)
real_down_2 = datetime_Bajada_Buena + datetime.timedelta(minutes=16)
real_down_3 = datetime_Bajada_Buena + datetime.timedelta(minutes=22)

hora_enciendeLuz = real_On.hour
minuto_enciendeLuz = real_On.minute
hora_bajada_1 = real_down_1.hour
minuto_bajada_1 = real_down_1.minute
hora_bajada_2 = real_down_2.hour
minuto_bajada_2 = real_down_2.minute
hora_bajada_3 = real_down_3.hour
minuto_bajada_3 = real_down_3.minute

# Si amanece antes de la hora que queremos no permite que las persianas suban antes
if amanece < hora_minima:
    amanece = hora_minima

enlaza = str(hoy)+" "+str(amanece)
from datetime import datetime # Esto es necesario aquí
datetime_Subida_Buena = datetime.strptime(enlaza, "%Y-%m-%d %H:%M:%S")
import datetime # Esto es necesario aquí
real_up_1 = datetime_Subida_Buena + datetime.timedelta(minutes=0)
real_up_2 = datetime_Subida_Buena + datetime.timedelta(minutes=1)
real_up_3 = datetime_Subida_Buena + datetime.timedelta(minutes=7)
hora_subida_1 = real_up_1.hour
minuto_subida_1 = real_up_1.minute
hora_subida_2 = real_up_2.hour
minuto_subida_2 = real_up_2.minute
hora_subida_3 = real_up_3.hour
minuto_subida_3 = real_up_3.minute

# Generamos el CRON nuevo en un archivo intermedio para poder volcarlo posteriormente al archivo en producción
## Llamamos a archivos de bash porque los de python a veces generan errores
file = open (rutaPrincipal+'CronPruebas','w')
file.write(str(cabecera)+ os.linesep)
file.write("#--------------------------------------------------------------------------------------------------"+ os.linesep)
file.write(str("#Este CRON ha sido generado en el instante ")+str(ahora)+ os.linesep)
file.write("#--------------------------------------------------------------------------------------------------"+ os.linesep)
file.write("#Código de control Automático de Persianas "+ os.linesep)
file.write("#--------------------------------------------------------------------------------------------------"+ os.linesep)
file.write("#Subimos las persianas Modo mañana de Lunes a Viernes"+ os.linesep)
file.write(str(minuto_subida_1)+" "+str(hora_subida_1)+" * * 1-5 sh /home/pi/source/TFG/scripts/control/GPIO_off.sh"+ os.linesep)
file.write(str(minuto_subida_2)+" "+str(hora_subida_2)+" * * 1-5 sh /home/pi/source/TFG/scripts/control/Subir.sh"+ os.linesep)
file.write(str(minuto_subida_3)+" "+str(hora_subida_3)+" * * 1-5 sh /home/pi/source/TFG/scripts/control/GPIO_off.sh"+ os.linesep)
file.write(""+ os.linesep)
file.write(str("#Subimos las persianas Modo mañana de Sabado y Domingo")+ os.linesep)
file.write(str("31 09 * * 6-7 sh /home/pi/source/TFG/scripts/control/GPIO_off.sh")+ os.linesep)
file.write(str("32 09 * * 6-7 sh /home/pi/source/TFG/scripts/control/Subir.sh")+ os.linesep)
file.write(str("38 09 * * 6-7 sh /home/pi/source/TFG/scripts/control/GPIO_off.sh")+ os.linesep)
file.write(""+ os.linesep)
file.write(str("#Encendemos las luces")+ os.linesep)
file.write(str(minuto_enciendeLuz)+" "+str(hora_enciendeLuz)+" * * * sh /home/pi/source/TFG/scripts/LucesOn.sh"+ os.linesep)
file.write(""+ os.linesep)
file.write(str("#Bajamos TODAS")+ os.linesep)
file.write(str(minuto_bajada_1)+" "+str(hora_bajada_1)+" * * * sh /home/pi/source/TFG/scripts/control/GPIO_off.sh"+ os.linesep)
file.write(str(minuto_bajada_2)+" "+str(hora_bajada_2)+" * * * sh /home/pi/source/TFG/scripts/control/Bajar.sh"+ os.linesep)
file.write(str(minuto_bajada_3)+" "+str(hora_bajada_3)+" * * * sh /home/pi/source/TFG/scripts/control/GPIO_off.sh"+ os.linesep)
file.write(""+ os.linesep)
file.write(str("#Apagamos las luces")+ os.linesep)
file.write(str(minuto_bajada_3)+" "+str(hora_bajada_3)+" * * * sh /home/pi/source/TFG/scripts/LucesOn.sh"+ os.linesep)
file.write(""+ os.linesep)
file.write(str("#Todos los días se  reinicia la máquina par que el demonio siempre esté correcto por la mañana")+ os.linesep)
file.write(str("05 04 * * * sudo reboot")+ os.linesep)
file.write(""+ os.linesep)
file.write(str("#Lanzamos el script de toma de horas")+ os.linesep)
file.write(str("05 00 * * * cd /home/pi/source/TFG/scripts/auto/ && sudo sh LanzaTodoElProceso.sh")+ os.linesep)
file.write(""+ os.linesep)

file.close()
# Log externo
file = open (rutaPrincipal+'log.cron','w')
file.write(str(hoy)+ os.linesep) 
file.write(str(ahora)+ os.linesep)
file.write(str("--------------------------------------")+ os.linesep)
file.write(str("Control de persianas:")+ os.linesep)
file.write(str("Amanece: ")+str(real_up_1)+os.linesep)
file.write(str("Luces: ")+str(real_On)+os.linesep)
file.write(str("Anochece: ")+str(real_down_1)+os.linesep)
file.close()

#print("Ha terminado el proceso de cálculo de horas.")


