#!/usr/bin/env python3
import urllib, json, datetime, pycurl, requests, os, obtencionDatos
import datetime, time
import pandas as pd 
import matplotlib.pyplot as plt

#Ip's que vamos a utilizar
#url_ip="http://ip-api.com/json/?fields=city,query,regionName"
url_tiempo = "https://api.climacell.co/v3/weather/forecast/hourly"
url_ip="http://ip-api.com/json/?fields=city,query,regionName,status,message,continent,continentCode,country,countryCode,region,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting"

#Obtenemos fecha de hoy y de mañana
ahora = time.ctime(time.time())
hoy=datetime.date.today()
fecha_manana = hoy + datetime.timedelta(1)

try:
    #En esta parte preparamos la conexi'ón de datos y las rutas a los archivos que necesitaremos
    tokenBot, users, KeyClimacell, KeyWeatherapi, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()

    #Calculamos ruta
    ruta=os.getcwd().split('/')
    rutaPrincipal=os.getcwd().split('/')

    # Hora más temprana de subida de persianas (configurable desde el bot)
    HoraMinima=rutaAuto+"2_condicionantes"
    f = open(HoraMinima)
    hora_minima = f.read()
    f.close()
    
    hm=hora_minima.split("\n")
    hora_minima = str(hm[1])
    temperatura = str(hm[3])[:5]


    print("hora minima:" + str(hora_minima) + " | temperatura: " + str(temperatura))

    #Leemos la cabecera del futuro archivo CRON, se puede obtener mediante 'cat' pero prefiero tener copia de seguridad.
    c = open (rutaAuto+'cabecera.txt')
    cabecera = c.read()
    c.close()
    
except Exception as e:
    print("Se ha producido un error en el módulo 1 de recabado de datos:"+str(e))

try:
    #Obtenemos toda la información de las APIS con la que trabajaremos posteriormente
    # Geolocalización
    sopa = requests.get(url_ip)
    prueba = sopa.json()
    ciudad = prueba['city']
    ip_publica = prueba['query']
    region = prueba['regionName']

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
            print("Ha habido un erroren la conexión al servidor de temperaturas")
        except:
            pass
    # Obtenemos el contenido de la url:
    sopa = requests.get(url_ip)

    # Tratamos los datos como json
    sopa_dict = dict(json.loads(sopa.content))

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
except Exception as e:
    print("Se ha producido un error en el módulo 2 de recabado de datos:"+str(e))

try:
    #Hacemos el cálculo de las horas para incluirlas en el CRON:
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
except Exception as e:
    print("Se ha producido un error en el módulo 2 de recabado de datos:"+str(e))

try:
    # Volcamos los datos al archivo de Información recabada

    file = open (rutaAuto+'InfoRecabada','w')
    file.write(str('{')+ os.linesep)
    file.write(str('"persianasSubir":\n\t{')+ os.linesep)
    file.write(str('\t"minuto_subida_1": ')+str(minuto_subida_1)+ os.linesep)
    file.write(str('\t"hora_subida_1": ')+str(hora_subida_1)+ os.linesep)
    file.write(str('\t"minuto_subida_2": ')+str(minuto_subida_2)+ os.linesep)
    file.write(str('\t"hora_subida_2": ')+str(hora_subida_2)+ os.linesep)
    file.write(str('\t"minuto_subida_3": ')+str(minuto_subida_3)+ os.linesep)
    file.write(str('\t"hora_subida_3": ')+str(hora_subida_3)+ os.linesep)
    file.write(str('\t}')+os.linesep)
    file.write(os.linesep)
    file.write(str('"luces":\n\t{')+ os.linesep)
    file.write(str('\t"minuto_enciendeLuz": ')+ str(minuto_enciendeLuz) + os.linesep)
    file.write(str('\t"hora_enciendeLuz": ')+ str(hora_enciendeLuz) + os.linesep)
    file.write(str('\t}')+os.linesep)
    file.write(os.linesep)
    file.write(str('"persianasBajar":\n\t{')+ os.linesep)
    file.write(str('\t"minuto_bajada_1": ')+str(minuto_bajada_1)+ os.linesep)
    file.write(str('\t"hora_bajada_1": ')+str(hora_bajada_1)+ os.linesep)
    file.write(str('\t"minuto_bajada_2": ')+str(minuto_bajada_2)+ os.linesep)
    file.write(str('\t"hora_bajada_2": ')+str(hora_bajada_2)+ os.linesep)
    file.write(str('\t"minuto_bajada_3": ')+str(minuto_bajada_3)+ os.linesep)
    file.write(str('\t"hora_bajada_3": ')+str(hora_bajada_3)+ os.linesep)
    file.write(str('\t}\n}')+os.linesep)
    file.write(os.linesep)
    file.write(os.linesep)
    file.close()
except Exception as e:
    print("Se ha producido un error en el módulo 3 de recabado de datos:"+str(e))










