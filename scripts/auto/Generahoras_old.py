import urllib, json, datetime, pycurl, requests, os 
import datetime
import pandas as pd 
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup #Web scrapping
url_ip="http://ip-api.com/json/?fields=city,query,regionName"
url_tiempo = "https://api.climacell.co/v3/weather/forecast/hourly"
id_weatherapi = "e60395a64bf647c29f984953200410"#Fecha mañana
hoy=datetime.date.today()
fecha_manana = hoy + datetime.timedelta(1)
sopa = requests.get(url_ip)
prueba = sopa.json()
ciudad = prueba['city']
ip_publica = prueba['query']
region = prueba['regionName']
url_tiempo = "http://api.weatherapi.com/v1/astronomy.json?key="+str(id_weatherapi)+"&q="+ciudad+"&dt="+str(fecha_manana)+""
resp = requests.get(url_tiempo)
diccionario = resp.json()
loc = diccionario['astronomy']
ast = loc['astro']
amanece = pd.to_datetime(ast['sunrise']).strftime('%H:%M:%S')
anochece = pd.to_datetime(ast['sunset']).strftime('%H:%M:%S')
enlaza = str(hoy)+" "+str(anochece)
media_hora =str(hoy)+" "+str('00:30:00')
from datetime import datetime # Esto es necesario aquí
datetime_Bajada_Buena = datetime.strptime(enlaza, "%Y-%m-%d %H:%M:%S")
import datetime # Esto es necesario aquí
real_down_1 = datetime_Bajada_Buena + datetime.timedelta(minutes=15)
real_down_2 = datetime_Bajada_Buena + datetime.timedelta(minutes=16)
real_down_3 = datetime_Bajada_Buena + datetime.timedelta(minutes=22)
hora_bajada_1 = real_down_1.hour
minuto_bajada_1 = real_down_1.minute
hora_bajada_2 = real_down_2.hour
minuto_bajada_2 = real_down_2.minute
hora_bajada_3 = real_down_3.hour
minuto_bajada_3 = real_down_3.minute
hora_minima = '08:00:00'
if amanece < hora_minima:
    amanece = hora_minima
amanece
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
c = open ('cabecera.txt','r')
cabecera = c.read()
c.close()
file = open ('CronPruebas','w')
file.write(cabecera+ os.linesep) 
file.write(" "+ os.linesep)
file.write("#Subimos las persianas Modo mañana de Lunes a Viernes"+ os.linesep)
file.write(str(minuto_subida_1)+" "+str(hora_subida_1)+" * * 1-5 sh /home/pi/Desktop/ScriptsPersianas/TiramoslosGPIO.sh"+ os.linesep)
file.write(str(minuto_subida_2)+" "+str(hora_subida_2)+" * * 1-5 sh /home/pi/Desktop/ScriptsPersianas/SubirMañanas.sh"+ os.linesep)
file.write(str(minuto_subida_3)+" "+str(hora_subida_3)+" * * 1-5 sh /home/pi/Desktop/ScriptsPersianas/TiramoslosGPIO.sh"+ os.linesep)
file.write(""+ os.linesep)
file.write(str("#Subimos las persianas Modo mañana de Sabado y Domingo")+ os.linesep)
file.write(str("31 09 * * 6-7 sh /home/pi/Desktop/ScriptsPersianas/TiramoslosGPIO.sh")+ os.linesep)
file.write(str("32 09 * * 6-7 sh /home/pi/Desktop/ScriptsPersianas/SubirMañanas.sh")+ os.linesep)
file.write(str("38 09 * * 6-7 sh /home/pi/Desktop/ScriptsPersianas/TiramoslosGPIO.sh")+ os.linesep)
file.write(""+ os.linesep)
file.write(str("#Bajamos las de la Zona Sur para que no de el SOL de Lunes a Viernes")+ os.linesep)
file.write(str("29 09 * * 1-5 sh /home/pi/Desktop/ScriptsPersianas/TiramoslosGPIO.sh")+ os.linesep)
file.write(str("30 09 * * 1-5 sh /home/pi/Desktop/ScriptsPersianas/SholMediaMañana.sh")+ os.linesep)
file.write(str("35 09 * * 1-5 sh /home/pi/Desktop/ScriptsPersianas/TiramoslosGPIO.sh")+ os.linesep)
file.write(""+ os.linesep)
file.write(str("#Bajamos las de la Zona Sur para que no de el SOL Sabado Y Domingo")+ os.linesep)
file.write(str("29 10 * * 6-7 sh /home/pi/Desktop/ScriptsPersianas/TiramoslosGPIO.sh")+ os.linesep)
file.write(str("30 10 * * 6-7 sh /home/pi/Desktop/ScriptsPersianas/SholMediaMañana.sh")+ os.linesep)
file.write(str("35 10 * * 6-7 sh /home/pi/Desktop/ScriptsPersianas/TiramoslosGPIO.sh")+ os.linesep)
file.write(""+ os.linesep)
file.write(str("#Subimos las de la zona sur para que ventile")+ os.linesep)
file.write(str("#05 20 * * * sh /home/pi/Desktop/ScriptsPersianas/TiramoslosGPIO.sh")+ os.linesep)
file.write(str("#06 20 * * * sh /home/pi/Desktop/ScriptsPersianas/VentilaNoche.sh")+ os.linesep)
file.write(str("#11 20 * * * sh /home/pi/Desktop/ScriptsPersianas/TiramoslosGPIO.sh")+ os.linesep)
file.write(""+ os.linesep)
file.write(str("#Bajamos TODAS")+ os.linesep)
file.write(str(minuto_bajada_1)+" "+str(hora_bajada_1)+" * * * sh /home/pi/Desktop/ScriptsPersianas/TiramoslosGPIO.sh"+ os.linesep)
file.write(str(minuto_bajada_2)+" "+str(hora_bajada_2)+" * * * sh /home/pi/Desktop/ScriptsPersianas/BajarTodas.sh"+ os.linesep)
file.write(str(minuto_bajada_3)+" "+str(hora_bajada_3)+" * * * sh /home/pi/Desktop/ScriptsPersianas/TiramoslosGPIO.sh"+ os.linesep)
file.write(""+ os.linesep)
file.write(str("#Todos los días se  reinicia la máquina par que el demonio siempre esté correcto por la mañana")+ os.linesep)
file.write(str("05 04 * * * sudo reboot")+ os.linesep)
file.write(""+ os.linesep)
file.write(str("#Lanzamos el script de toma de horas")+ os.linesep)
file.write(str("05 00 * * * cd /home/pi/Desktop/Generador/ && sudo sh LanzaTodoElProceso.sh")+ os.linesep)
file.write(""+ os.linesep)
file.close()
file = open ('log.cron','w')
file.write(str(hoy)+ os.linesep) 
file.close()