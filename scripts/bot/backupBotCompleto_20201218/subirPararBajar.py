
def controlPersianas(m, bot):
    try:
        import os, obtencionDatos
        
        tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()
        usuario = m.chat.id
        
        todos=[]
        for i in persianas:
            todos.append(i[1])
            todos.append(i[2])

        if ((len(m.text.split(" "))==1) and(m.text[1:]=="parar")):
            bot.send_message(usuario, "Paramos todas las persianas")
            for pin in todos:
                os.system("gpio -g mode "+pin+" in")
            bot.send_message(usuario, "Persianas paradas")
        
        elif ((len(m.text.split(" "))==3) and (sum((m.text.split(" ")[1]) in string for string in persianas)>0)):
            condiciones=m.text.split(" ")
            if m.text.split(" ")[0][1:]=="subir": posicion=1
            if m.text.split(" ")[0][1:]=="bajar": posicion=2
            
            # Obtenemos los pines de la persiana 
            for i in persianas:
                if (i[0]==str(m.text.split(" ")[1])):
                    pinSube = i[1]
                    pinBaja = i[2]

            if condiciones[0][1:]=="subir":
                bot.send_message(usuario, "Subimos la persiana de "+str(m.text.split(" ")[1]))
                tiempo=str(m.text.split(" ")[2])
                os.system("gpio -g mode "+pinSube+" out")
                os.system("sleep "+str(m.text.split(" ")[2]))
                os.system("gpio -g mode "+pinSube+" in")
                bot.send_message(usuario, "Persiana parada")
                
            if condiciones[0][1:]=="bajar": 
                bot.send_message(usuario, "Bajamos la persiana de "+str(m.text.split(" ")[1]))
                os.system("gpio -g mode "+pinBaja+" out")
                os.system("sleep "+m.text.split(" ")[2])
                os.system("gpio -g mode "+pinBaja+" in")
                bot.send_message(usuario, "Persiana parada")
        else:
            bot.send_message(usuario, "No reconozco el comando, puedes probar con:")
            bot.send_message(usuario, "/parar, /subir ubicación tiempo, /bajar ubicación tiempo") 

    except:
        bot.send_message(usuario, "No reconozco el comando, puedes probar con:")
        bot.send_message(usuario, "/parar, /subir ubicación tiempo, /bajar ubicación tiempo")   
