def generador(m, bot):
    try:
        import os, obtencionDatos
        from telegram import ParseMode
        
        usuario = m.chat.id
        tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()
        
        import os, obtencionDatos        
        os.system("python3.7 "+rutaAuto+"1_recabaInfo.py")
        os.system("python3.7 "+rutaAuto+"3_cocinado.py")
        os.system("sh " + rutaAuto+"4_reescribeCron.sh")

        #Leemos información del archivo        
        f = open(rutaAuto+"log.cron", "r")
        data = f.read()
        f.close()
    
        #Obtenemos la primera línea aunque se puede cambiar a la segunda...
        matrix1 = data.split('\n')
        bot.send_message(usuario, "Datos obtenidos el "+matrix1[0]+" a las "+matrix1[1].split(' ')[3] + "ya implantados.")
    except Exception as e:
        bot.send_message(usuario, "Error en módulo de obtención de datos: " + str(e))
