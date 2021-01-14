def calefaccion(m, bot):
    try:
        import os, obtencionDatos
        from telegram import ParseMode
        
        usuario = m.chat.id
        tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()
        
        comandos=m.text.split(" ")
        f = open(rutaAuto+"2_condicionantes", "r")
        dataOriginal = f.read()
        f.close()
        
        data = dataOriginal.split("\n")
        
        temp=data[3]
        
        if len(comandos)==1:
            bot.send_message(usuario, "La temperatura está fijada en <b>"+temp+ "</b>ºC &#128293;",parse_mode=ParseMode.HTML)    
        
        if len(comandos)==2:
            try:
                tempNueva=float(comandos[1][0:5].replace(",","."))
            except Exception as e:
                tempNueva=temp
                bot.send_message(usuario, "Debes introducir valores numéricos")
                
            f = open(rutaAuto+"2_condicionantes", "w")
            f.write(str(data[0]) + os.linesep)
            f.write(str(data[1]) + os.linesep)
            f.write(str(data[2]) + os.linesep)
            f.write(str(tempNueva) + os.linesep)
            f.close()
            
            os.system("python3.7 "+rutaAuto+"3_cocinado.py")
            os.system("sh " + rutaAuto+"4_reescribeCron.sh")
            
            f = open(rutaAuto+"2_condicionantes", "r")
            dataOriginal = f.read()
            f.close()
            
            data = dataOriginal.split("\n")
            
            temp=data[3]
            if tempNueva!=temp:
                bot.send_message(usuario, "La temperatura se ha fijado en <b>"+temp+ "</b>ºC &#128293;",parse_mode=ParseMode.HTML)
            else:
                bot.send_message(usuario, "La temperatura continúa fijada en <b>"+temp+ "</b>ºC &#128293;",parse_mode=ParseMode.HTML)    
    except Exception as e:
        bot.send_message(usuario, "Error en el módulo de calefacción: "+str(e))
