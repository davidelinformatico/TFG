def datos(m, bot):
    try:
        import os, obtencionDatos, time, datetime
        from telegram import ParseMode
        
        usuario = m.chat.id
        tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()
        
        #Leemos información del archivo        
        f = open(rutaAuto+"log.cron", "r")
        data = f.read()
        f.close()

        bot.send_chat_action(usuario, 'typing')
        time.sleep(1)

        #Obtenemos la primera línea aunque se puede cambiar a la segunda...
        matrix1 = data.split('\n')
        
        mm = str("Datos generados el <b>"+matrix1[0]+"</b> a las <strong>"+matrix1[1].split(' ')[3]+str("</strong>:\n<pre>|"))
        mm += matrix1[4].split(" ")[0]+str("  | ")+matrix1[4].split(" ")[2]+ str(" | &#127774; \n|")
        mm += matrix1[5].split(" ")[0]+str("    | ")+matrix1[5].split(" ")[2]+ str(" | &#128161; \n|")
        mm += matrix1[6].split(" ")[0]+str(" | ")+matrix1[6].split(" ")[2]+ str(" | &#127770; \n</pre>")

        bot.send_message(usuario, text=mm, parse_mode=ParseMode.HTML)
       
    except:
        bot.send_message(usuario, "Error en la lectura del archivo")


        
        