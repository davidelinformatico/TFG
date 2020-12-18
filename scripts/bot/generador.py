def generador(m, bot):
    try:
        import os, obtencionDatos        
        p = os.popen("bash " +rutaAuto+"LanzaTodoElProceso.sh")

        #Leemos información del archivo        
        f = open(rutaAuto+"log.cron", "r")
        data = f.read()
        f.close()
    
        #Obtenemos la primera línea aunque se puede cambiar a la segunda...
        matrix1 = data.split('\n')
        bot.send_message(usuario, "Datos obtenidos el "+matrix1[0]+" a las "+matrix1[1].split(' ')[3])
    except:
        bot.send_message(usuario, "Error!\n")
