def datos(m, bot):
    '''
    Este método recibe el mensaje enviado por el usuario y la información del bot que lo recoge.
    Posteriormente recibe las rutas necesarias de obtencionDatos para llegar al archivo de consultas
    log.cron, donde obtiene la información del movimiento de las persianas y de salida y puesta de sol.

    @params m, mensaje recogido por el listener; bot, información del bot
    @return nothing
    @send envía mensaje informativo al usuario
    '''
    import os, obtencionDatos, time, datetime
    from telegram import ParseMode
    
    usuario = m.chat.id
    tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()

    try:
        #Leemos información del archivo        
        f = open(rutaAuto+"log.cron", "r")
        data = f.read()
        f.close()

        bot.send_chat_action(usuario, 'typing')
        time.sleep(1)

        #Obtenemos la primera línea aunque se puede cambiar a la segunda...
        matrix1 = data.split('\n')
        
        mm = str("Datos generados el <b>"+matrix1[0]+"</b> a las <strong>"+matrix1[1].split(' ')[3]+str("</strong>:\n<pre>|"))
        mm += str(" Amanecer Ubicac | ")+matrix1[5].split(" ")[4]+ str(" | &#127749; \n|")
        mm += str(" Subir Persianas | ")+matrix1[6].split(" ")[3]+ str(" | &#127773; \n|")
        mm += str(" Encendido luces | ")+matrix1[7].split(" ")[3]+ str(" | &#128161; \n|")
        mm += str(" Bajar Persianas | ")+matrix1[7].split(" ")[3]+ str(" | &#127770; \n</pre>")

        print(mm)
        bot.send_message(usuario, text=mm, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        bot.send_message(usuario, "Error en el módulo de datos: "+str(e))
        print("Error en el módulo de datos: "+str(e))

        
        