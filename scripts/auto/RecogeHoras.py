#!/usr/bin/env python3
import urllib, json, pycurl, requests, datetime, os, time, stat
from datetime import date
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib
    
#Calculamos ruta
ruta=os.getcwd().split('/')
rutaPrincipal=os.getcwd().split('/')
salida=""
for i in range(len(ruta)-3):
    salida=str(salida)+"/"+str(ruta[i])
ruta=salida[1:]+str("/credentials/")

cosa=""
for i in range(len(rutaPrincipal)-1):
    cosa=str(cosa)+"/"+str(rutaPrincipal[i])
rutaPrincipal=cosa[1:]+str("/auto/")

try:
    print("Ha comenzado el proceso de cálculo de temperaturas.")
except:
    pass
# Obtención de los seriales

# Llamamos a mi key personal de Climacell, que está en otro directorio.
result = open(ruta+'KeyClimacell')
KeyClimacell = result.read()
result.close()

# Temperatura a la que encenderemos la calefacción
f = open(rutaPrincipal+'TemperaturaCalefaccion')
temperatura = f.read()
f.close()

#Ip's que vamos a utilizar
url_ip="http://ip-api.com/json/?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
url_tiempo = "https://api.climacell.co/v3/weather/forecast/hourly"

# Obtenemos la fecha del día en curso:
fecha_hoy = date.today()
# Obtenemos la fecha del día de mañana:
fecha_manana = fecha_hoy + datetime.timedelta(days=1)

# Requests conecta con la web y devuelve <Response [200]> si ha conectado correctamente. Lo almacenamos en response.
try:
    response = requests.get(url_ip)
except:
    try:
        response = -1000
        print("No se puede comunicar con la web!!")
    except:
        pass
# Comprobamos si la conexión devuelve el valor de correcta conexión '<Response [200]>'
respuesta=str(response).find("<Response [200]>")
if respuesta != -1:
    try:
        print("Se ha conectado correctamente")
    except:
        pass
else:
    try:
        print("Ha habido un error")
    except:
        pass

# Obtenemos el contenido de la url:
sopa = requests.get(url_ip)

# Tratamos los datos como json
sopa_dict = dict(json.loads(sopa.content))

# Obtenemos los valores que necesitamos para el tiempo
ciudad = sopa_dict['city']
region = sopa_dict['regionName']
ip_publica = sopa_dict['query']
LAT = sopa_dict['lat']
LON = sopa_dict['lon']
ISP = sopa_dict['isp']

# Montamos la consulta
querystring = {"lat": LAT,"lon": LON,"unit_system":"si","start_time":"now","fields":"temp","apikey": KeyClimacell}
# Recogemos la "sopa" de datos
sopa_tiempo = requests.request("GET", url_tiempo, params=querystring)

# Convertimos a json
sopa_tiempo_json = sopa_tiempo.json()

#--------------------------------------------------------------------------------
## SE CONSULTA LAS TEMPERATURAS DEL DIA SIGUIENTE PARA PODER INCLUIRLO EN CRON
#--------------------------------------------------------------------------------
# Como vamos a tratar las horas y temperaturas como un diccionario:
th = {}
# Guardamos fecha
b = str(fecha_manana)
try:
    print("")
except:
    pass

#print("De esta manera obtenemos la hora y la temperatura del día de mañana:")
for i in range (100):
    a = (str(sopa_tiempo_json[i]['observation_time']['value'][:10]))
    #print(a)
    if (a == b):
        th[i] = str(sopa_tiempo_json[i]['observation_time']['value'][11])+str(sopa_tiempo_json[i]['observation_time']['value'][12])+":"+str(sopa_tiempo_json[i]['temp']['value'])
        #print(th[i])

# Pasamos los valores a lista
lista = list(th.values())
# Creamos un diccionario final
temperatura_hora={}

# Introducimos las temperaturas en el nuevo diccionario
for i in range (24):
    #lista[i][:2]
    temperatura_hora[i]=float(lista[i][3:])

# Ordenamos los valores por la hora
lists = sorted(temperatura_hora.items())

try:
    # Hacemos las asignaciones x,y
    x, y = zip(*lists) 

    fig = plt.figure(dpi=600)
    fig.set_figwidth(11)

    plt.grid()
    plt.title("Temperaturas día "+b)
    plt.xlabel("Horas")
    plt.ylabel("Temperatura C")
    plt.xticks([i for i in range(24)]) 

    # Corrección y graficado de las temperaturas del día de mañana
    plt.plot(x, y)

    # Exportamos imagen con la fecha como nombre
    os.chdir(rutaPrincipal+"diagramas")
    plt.savefig(b+".png")
    plt.clf()
    plt.cla()
    plt.close()
    os.chmod(b+".png", stat.S_IRWXU) # Cambiamos lo permisos para que el usuario pueda sobreescribirlo
    #os.chmod(b+".png", stat.S_IRWXG)
    #os.chmod(b+".png", stat.S_IRWXO)
except Exception as e:
    print("Error en imagen:")
    print(e)


# Calculamos la hora a la que tenemos más temperatura
hora_maxima = max(temperatura_hora, key=temperatura_hora.get)

# Calculamos la hora a la que tenemos menos temperatura
hora_minima = min(temperatura_hora, key=temperatura_hora.get)

# Pin caldera: GPIO 10, pin 19


#Abrimos el archivo
os.chdir(rutaPrincipal)
file = open ('CronPruebas','a')
file.write(""+ os.linesep)
file.write("# Comprueba cada minuto que el bot está corriendo"+ os.linesep)
file.write("* * * * * sh /home/pi/source/TFG/scripts/bot/compuebaBot.sh"+ os.linesep)
file.write(""+ os.linesep)
file.write("#--------------------------------------------------------------------------------------------------"+ os.linesep)
file.write("#Código de control Automático de Calefacción "+ os.linesep)
file.write("#--------------------------------------------------------------------------------------------------"+ os.linesep)
file.write(" "+ os.linesep)

# Generamos el encendido de la caldera y calefacción
for hora in temperatura_hora:
    if (temperatura_hora[hora] <= int(temperatura)):
        #Apagar caldera
        file.write("0 "+str(hora)+" * * 1-7 sh /home/pi/source/TFG/scripts/control/EncenderCaldera.sh"+ os.linesep)
        #file.write(str("38 09 * * 6-7 sh /home/pi/source/TFG/scripts/control/GPIO_off.sh")+ os.linesep)

    else:
        #Apagar caldera
        file.write("0 "+str(hora)+" * * 1-7 sh /home/pi/source/TFG/scripts/control/ApagarCaldera.sh"+ os.linesep)


file.write(""+ os.linesep)
file.write(""+ os.linesep)
file.close()

file = open (rutaPrincipal+'log.cron','a')
file.write(str("--------------------------------------")+ os.linesep)
file.write(str("Temperaturas por horas:")+ os.linesep)
file.write(str("--------------------------------------")+ os.linesep)
for i in lists:
    file.write(str(i)+ os.linesep)


file.write(""+ os.linesep)
file.write(""+ os.linesep)

file.close()

try:
    print("Ha terminado el proceso de cálculo de temperaturas.")
except:
    pass





