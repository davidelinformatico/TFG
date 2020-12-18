def temperaturas(m, bot):
    try:
        import os, obtencionDatos, sys, time, datetime
        from telegram import ParseMode
        usuario = m.chat.id
        tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()
        
        try:
            #Leemos información del archivo
            f = open(rutaAuto+"log.cron", "r")
            data = f.read()
            f.close()
        except Exception as e:
            print("Error en "+e)
        
        bot.send_chat_action(usuario, 'typing')
        time.sleep(1)
        #Obtenemos la primera línea aunque se puede cambiar a la segunda...
        matrix1 = data.split('\n')
        bot.send_message(usuario, "Las temperaturas por hora son:")

        ss = str(int(matrix1[4].split(" ")[2].split(":")[0]))
        ll = matrix1[5].split(" ")[2].split(":")[0]
        bb = matrix1[6].split(" ")[2].split(":")[0]

        try:
            compilado = "|  Hora  |Temperatura|"
            for i in range(len(matrix1)-1):
                if ((i >10) and (i<20)):
                    compilado += str("\n|    ")+matrix1[i].split(", ")[0][1:]
                    if len(matrix1[i].split(", ")[1][:-1])==3:
                        compilado += str("   |  ")+matrix1[i].split(", ")[1][:-1]+str(" ºC   |")
                    if len(matrix1[i].split(", ")[1][:-1])==4:
                        compilado += str("   |  ")+matrix1[i].split(", ")[1][:-1]+str(" ºC  |")
                    if len(matrix1[i].split(", ")[1][:-1])==5:
                        compilado += str("   |  ")+matrix1[i].split(", ")[1][:-1]+str(" ºC |")
                    if (matrix1[i].split(", ")[0][1:]==ss):
                        compilado += str("&#127774;")+str(matrix1[4].split(" ")[2][:-3])
                    #print("-->"+matrix1[i].split(", ")[0][1:]+" |"+ss)
                if ((i >=20) and (i<34)):
                    compilado += str("\n|   ")+matrix1[i].split(", ")[0][1:]
                    if len(matrix1[i].split(", ")[1][:-1])==3:
                        compilado += str("   |  ")+matrix1[i].split(", ")[1][:-1]+str(" ºC   |")                    
                    if len(matrix1[i].split(", ")[1][:-1])==4:
                        compilado += str("   |  ")+matrix1[i].split(", ")[1][:-1]+str(" ºC  |")
                    if len(matrix1[i].split(", ")[1][:-1])==5:
                        compilado += str("   |  ")+matrix1[i].split(", ")[1][:-1]+str(" ºC |")
                    if (matrix1[i].split(", ")[0][1:]==ss):
                        compilado += str("&#127774;")+str(matrix1[4].split(" ")[2][:-3])
                    if (matrix1[i].split(", ")[0][1:]==bb):
                        compilado += str("&#128161;&#127770;")+str(matrix1[5].split(" ")[2][:-3])
        except Exception as e:
            print("Error en la generación del mensaje: "+e)
        #print(compilado)
        bot.send_message(usuario, text='<pre><code class="language-python">'+compilado+'</code></pre>', parse_mode=ParseMode.HTML)

        
    except:
        bot.send_message(usuario, "Error en la lectura del archivo")
