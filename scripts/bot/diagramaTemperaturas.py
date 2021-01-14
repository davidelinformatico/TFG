def diagrama(m, bot, pwdBot):
    '''
    Este método recibe el mensaje enviado por el usuario y la información del bot que lo recoge y su
    ubicación en la máquina.
    Posteriormente recibe las rutas necesarias de obtencionDatos para llegar a los diagramas.
    En caso de existir una imagen se envía la última imagen generada.
    En caso de solicitar una imagen existente envía esa imagen.
    En caso de no existir, envía mensaje informativo al usuario

    @params m, mensaje recogido por el listener; bot, información del bot; pwdBot, ubicación del bot
    @return nothing
    @send envía imagen al usuario
    '''
    try:
        import os, obtencionDatos
        
        usuario = m.chat.id
        tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()

        # Obtenemos la 'última imagen dentro de la ruta de imágenes
        pwdImagenes = rutaAuto+"diagramas/"
        os.chdir(pwdImagenes)
        result = os.popen('ls -r').read()
        imagenPorDefecto=((result.split("\n"))[0])
        os.chdir(pwdBot)
        
        imagenDefecto=(str(pwdImagenes)+str(imagenPorDefecto))
        
        if ((len(m.text[len("/d "):])) > 0):
            nombre= str(m.text[len("/d "):])
            imagenUsuario=(str(pwdImagenes)+str(nombre)+".png")
            bot.send_photo(usuario,photo=open(imagenUsuario, 'rb'))
        else:
            bot.send_photo(usuario,photo=open(imagenDefecto, 'rb'))
    except:
        tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()
        pwdImagenes = rutaAuto+"diagramas/"
        os.chdir(pwdImagenes)
        bot.send_message(usuario, "Error. Prueba con alguna de estas con formato AAAA-MM-DD:\n")
        result = os.popen('ls -r | rev | cut -f 2- -d "." | rev').read()
        cosa=(result.split("\n"))
        
        try:
            #Últimas 10 imágenes para no recargar la salida
            for i in range(len(cosa)):
                if i<5:
                    bot.send_message(usuario, cosa[i])
                    print(cosa[i])
                    i=i+1
        except Exception as e:
            print("El bucle ha tenido un error: "+str(e))
