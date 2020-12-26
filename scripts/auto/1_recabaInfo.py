#!/usr/bin/env python3
import urllib, json, datetime, pycurl, requests, os, obtencionDatos, stat
import datetime, time
import pandas as pd 
import matplotlib.pyplot as plt

#Ip's que vamos a utilizar
url_ip = "http://ip-api.com/json/?fields=city,query,regionName,status,message,continent,continentCode,country,countryCode,region,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting"
url_tiempo = "https://api.climacell.co/v3/weather/forecast/hourly"

#Obtenemos fecha de hoy y de mañana
ahora = time.ctime(time.time())
hoy=datetime.date.today()
fecha_manana = hoy + datetime.timedelta(1)

try:
    #En esta parte preparamos la conexión de datos y las rutas a los archivos que necesitaremos
    tokenBot, users, KeyClimacell, KeyWeatherapi, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()
    
    #Calculamos ruta
    ruta=os.getcwd().split('/')
    rutaPrincipal=os.getcwd().split('/')

   
except Exception as e:
    print("Se ha producido un error en el módulo 1 de recabado de datos:"+str(e))

try:
    #Obtenemos toda la información de las APIS con la que trabajaremos posteriormente
    # Geolocalización
    try:
        sopa = requests.get(url_ip)
    except Exception as e:
        print("Error al hacer la sopa: "+str(e))
    
    prueba = sopa.json()
    ciudad = prueba['city']
    ip_publica = prueba['query']
    region = prueba['regionName']
    LAT = prueba['lat']
    LON = prueba['lon']


    # Montamos la consulta
    querystring = {"lat": LAT,"lon": LON,"unit_system":"si","start_time":"now","fields":"temp","apikey": KeyClimacell}
    # Recogemos la "sopa" de datos
    sopa_tiempo = requests.request("GET", url_tiempo, params=querystring)
    
    #print(sopa_tiempo.text)

    # Convertimos a json
    sopa_tiempo_json = sopa_tiempo.json()
    #---------------------------------------------------------------
    
    #Tiempo mañana en la ubicación de la máquina
    url_tiempo = "http://api.weatherapi.com/v1/astronomy.json?key="+str(KeyWeatherapi)+"&q="+ciudad+"&dt="+str(fecha_manana)+""
    resp = requests.get(url_tiempo)
    diccionario = resp.json()
    loc = diccionario['astronomy']
    ast = loc['astro']
    #Hora en que amanece y anochece en formato 24h
    amanece = pd.to_datetime(ast['sunrise']).strftime('%H:%M:%S')
    anochece = pd.to_datetime(ast['sunset']).strftime('%H:%M:%S')
    enlaza = str(hoy)+" "+str(anochece)
    media_hora =str(hoy)+" "+str('00:30:00')
    
    # Como vamos a tratar las horas y temperaturas como un diccionario:
    th = {}
    # Guardamos fecha
    b = str(fecha_manana)

    #print("De esta manera obtenemos la hora y la temperatura del día de mañana:")
    for i in range (100):
        a = (str(sopa_tiempo_json[i]['observation_time']['value'][:10]))
        #print(a)
        if (a == b):
            th[i] = str(sopa_tiempo_json[i]['observation_time']['value'][11])+str(sopa_tiempo_json[i]['observation_time']['value'][12])+":"+str(sopa_tiempo_json[i]['temp']['value'])

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
    #print(lists)

except Exception as e:
    print("Se ha producido un error en el módulo 2 de recabado de datos:"+str(e))

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
    os.chdir(rutaAuto+"diagramas")
    plt.savefig(b+".png")
    plt.clf()
    plt.cla()
    plt.close()
    os.chmod(b+".png", stat.S_IRWXU) # Cambiamos lo permisos para que el usuario pueda sobreescribirlo

except Exception as e:
    print("Error en imagen: "+str(e))


try:
    # Volcamos los datos al archivo de Información recabada
    file = open (rutaAuto+'InfoRecabada','w')
    file.write(str('{')+ os.linesep)
    file.write(str('"Planeta":\n\t{')+ os.linesep)
    file.write(str('\t"Amanecer": "')+str(amanece)+ str('",') + os.linesep)
    file.write(str('\t"Anochecer": "')+str(anochece)+ str('"') + os.linesep)
    file.write(str('\t},')+os.linesep)
    file.write(os.linesep)
    file.write(str('"temperaturas":\n\t{')+ os.linesep)
    for hora in lists:
        if (int(hora[0])==23):
            file.write(str('\t"')+str(hora[0])+str('": ')+str(hora[1]) + os.linesep)
        else:
            file.write(str('\t"')+str(hora[0])+str('": ')+str(hora[1]) + str(',') + os.linesep)
    file.write(str('\t}\n}')+os.linesep)
    file.write(os.linesep)
    file.close()
except Exception as e:
    print("Se ha producido un error en el módulo 3 de recabado de datos:"+str(e))


f = open(rutaAuto+'InfoRecabada')
data = f.read()
f.close()

print(data)