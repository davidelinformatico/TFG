#!/usr/bin/env python3
import urllib, json, datetime, pycurl, requests, os, obtencionDatos, stat, datetime, time, obtencionDatos
#from datetime import datetime

tokenBot, users, KeyClimacell, KeyWeatherapi, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()

#try:
#Lectura de archivo de datos
f = open(rutaAuto+'InfoRecabada', "r")
data = json.loads(f.read()) 
f.close()

# Hora más temprana de subida de persianas (configurable desde el bot)
f = open("2_condicionantes")
condicionantes = f.read()
f.close()

cond=condicionantes.split("\n")
horaMinima = cond[1]
tempCalefaccion = float(cond[3].replace(',', '.'))

#Leemos la cabecera del futuro archivo CRON, se puede obtener mediante 'cat' pero prefiero tener copia de seguridad.
c = open (rutaAuto+'cabecera.txt')
cabecera = c.read()
c.close()

#print(horaMinima)
#print(tempCalefaccion)

#except Exception as e:
#    print("Error en en módulo 1 de lectura de archivos"+str(e))

try:
    ahora = time.ctime(time.time())
    hoy=datetime.date.today()
    fecha_manana = hoy + datetime.timedelta(1)
    
    enlaza = str(hoy)+" "+str(data["Planeta"]["Anochecer"])
    media_hora =str(hoy)+" "+str('00:30:00')

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
    #if amanece < hora_minima:
    #    amanece = hora_minima

    planetaAmanece = str(hoy)+" "+str(data["Planeta"]["Amanecer"])
    horaPersianas = str(hoy)+" "+str(horaMinima)
    
    if planetaAmanece < horaPersianas:
        enlaza = horaPersianas
    else:
        enlaza = planetaAmanece

    #enlaza = str(hoy)+" "+str(amanece)
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
    print("Error en el módulo 2, de cálculo: "+str(e))

try:
    # Generamos el CRON nuevo en un archivo intermedio para poder volcarlo posteriormente al archivo en producción
    ## Llamamos a archivos de bash porque los de python a veces generan errores
    file = open (rutaAuto+'CronPruebas','w')
    file.write(str(cabecera)+ os.linesep)
    file.write("#--------------------------------------------------------------------------------------------------"+ os.linesep)
    file.write(str("#Este CRON ha sido generado en el instante ")+str(ahora)+ os.linesep)
    file.write("#--------------------------------------------------------------------------------------------------"+ os.linesep)
    file.write("#Código de control Automático de Persianas "+ os.linesep)
    file.write("#--------------------------------------------------------------------------------------------------"+ os.linesep)
    file.write("#Subimos las persianas Modo mañana de Lunes a Domingo"+ os.linesep)
    file.write(str(minuto_subida_1)+" "+str(hora_subida_1)+" * * * sh /home/pi/source/TFG/scripts/control/GPIO_off.sh"+ os.linesep)
    file.write(str(minuto_subida_2)+" "+str(hora_subida_2)+" * * * sh /home/pi/source/TFG/scripts/control/Subir.sh"+ os.linesep)
    file.write(str(minuto_subida_3)+" "+str(hora_subida_3)+" * * * sh /home/pi/source/TFG/scripts/control/GPIO_off.sh"+ os.linesep)

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

    
    #file = open ('CronPruebas','a')
    file.write(""+ os.linesep)
    file.write("#--------------------------------------------------------------------------------------------------"+ os.linesep)
    file.write("#Código de control Automático de Calefacción "+ os.linesep)
    file.write("#--------------------------------------------------------------------------------------------------"+ os.linesep)
    file.write(" "+ os.linesep)

        
    for i in range(len(data["temperaturas"])):
        if (data["temperaturas"][str(i)] <= tempCalefaccion):
            #Apagar caldera
            file.write("0 "+str(i)+" * * 1-7 sh /home/pi/source/TFG/scripts/control/EncenderCaldera.sh"+ os.linesep)
        else:
            #Apagar caldera
            file.write("0 "+str(i)+" * * 1-7 sh /home/pi/source/TFG/scripts/control/ApagarCaldera.sh"+ os.linesep)

    file.write(""+ os.linesep)
    file.write(""+ os.linesep)

    file.close()
    
    # Log externo
    file = open (rutaAuto+'log.cron','w')
    file.write(str(hoy)+ os.linesep) 
    file.write(str(ahora)+ os.linesep)
    file.write(str("--------------------------------------")+ os.linesep)
    file.write(str("Control de persianas:")+ os.linesep)
    file.write(str("Amanece en casa: ")+str(planetaAmanece)+os.linesep)
    file.write(str("Persianas Suben: ")+str(real_up_1)+os.linesep)
    file.write(str("Encendido Luces: ")+str(real_On)+os.linesep)
    file.write(str("Persianas Bajan: ")+str(real_down_1)+os.linesep)
    file.close()

except Exception as e:
    print("Error en el módulo de grabado de CRON: "+str(e))