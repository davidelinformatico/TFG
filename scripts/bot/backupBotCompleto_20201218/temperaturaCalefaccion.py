def calefaccion(m, bot):
    try:
        import os, obtencionDatos
        from telegram import ParseMode
        
        usuario = m.chat.id
        tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()
        
        comandos=m.text.split(" ")
        f = open(rutaAuto+"TemperaturaCalefaccion")
        temp = f.read()
        f.close()
        
        if len(comandos)==1:
            bot.send_message(usuario, "La temperatura está fijada en <b>"+temp+ "</b>ºC &#128293;",parse_mode=ParseMode.HTML)    
        
        if len(comandos)==2:
            horaNueva=comandos[1][0:5]
            f = open(rutaAuto+"TemperaturaCalefaccion", "w")
            f.write(str(horaNueva))
            f.close()
            
            f = open(rutaAuto+"TemperaturaCalefaccion")
            temp = f.read()
            f.close()
            bot.send_message(usuario, "La temperatura se ha fijado en <b>"+temp+ "</b>ºC &#128293;",parse_mode=ParseMode.HTML)    
    except:
        pass
