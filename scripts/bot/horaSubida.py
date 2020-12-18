def horaSubida(m, bot):
    try:
        import os, obtencionDatos
        from telegram import ParseMode
        
        usuario = m.chat.id
        tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()

        # Leemos hora antigua
        f = open(rutaAuto+"HoraMinima")
        horaAntigua = f.read()
        f.close()

        # Leemos la hora introducida por parámetro
        horaNueva=str((m.text[len("/cambiar"):].split())[0])

        if len(horaNueva)==5:
            horaNueva += str(":00")
            f = open(rutaAuto+"HoraMinima", "w")
            f.write(str(horaNueva))
            f.close()
            
            #Comprobamos el cambio de hora
            f = open(rutaAuto+"HoraMinima")
            horaNueva = f.read()
            f.close()
            #Leemos hora a cambiar
            bot.send_message(usuario, "La hora ha cambiado de <i>"+str(horaAntigua[:-3]) + "</i> a <b>"+str(horaNueva[:-3])+"</b> &#128337;",parse_mode=ParseMode.HTML)
        else:
            bot.send_message(usuario, "Introduce el formato correcto: HH:MM")    
    except:
        bot.send_message(usuario, "Debes introducir una hora con formato HH:MM\n")

def consulta(m ,bot):
    try:
        import os, obtencionDatos, datetime, time
        from telegram import ParseMode
        
        usuario = m.chat.id
        tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()
        
        # Leemos hora antigua
        f = open(rutaAuto+"HoraMinima")
        horaAntigua = f.read()
        f.close()
   
        bot.send_chat_action(usuario, 'typing')
        time.sleep(1)
        
        bot.send_message(usuario, "Las persianas se subirán como pronto a las <b>"+str(horaAntigua[:-3]) + "</b> &#128337;",parse_mode=ParseMode.HTML)

    except:
        bot.send_message(usuario, "Error al obtener la hora")





