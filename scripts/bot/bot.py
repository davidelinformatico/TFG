import telebot, logging, subprocess, telegram
import os, obtencionDatos,time, requests, datetime, sys
from telebot import types
from telegram import ParseMode


# Registro de eventos
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('SDI_domo.log')

#Diccionario con los comandos disponibles en el bot.
commands = {
             'ayuda': 'Muestra información sobre los comandos',
             #'e': 'Ejecuta un comando',
             'subir': 'Subir persianas',
             'bajar': 'Bajar persianas',
             'parar': 'Para las persianas',
             'temp': 'Listado de temperaturas',
             'd': 'Diagrama de temperaturas',
             'cambiar': 'Cambiar hora subida',
             'datos': 'Hora de recopilación de datos',
             'hora': 'Hora a la que suben las persianas',
             'generar': 'Genera los archivos de control',
             'info': 'Información de la RaspberryPi',
             'apagar': ' Apagar sistema domótico',
             'reiniciar': 'Reinicia la Raspberry PI'
            }

# Configuración básica de nuestro Bot
def configBot():
    #Calculamos ruta
    pwdBot=os.getcwd()
    rutaPrincipal=pwdBot.split('/')
    ruta=pwdBot.split('/')
    salida=""
    for i in range(len(ruta)-3):
        salida=str(salida)+"/"+str(ruta[i])
    rutaCred=salida[1:]+str("/credentials/")

    cosa=""
    for i in range(len(rutaPrincipal)-1):
        cosa=str(cosa)+"/"+str(rutaPrincipal[i])
    rutaAuto=cosa[1:]+str("/auto/")

    tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()

    # Leemos el archivo
    f = open(rutaCred+"config2.bot")
    data = f.read()
    f.close()
        
    # Preparamos los datos cortando por los saltos de línea
    datos = data.split('\n')
    
    #Obtenemos el Token
    bot = telebot.TeleBot(tokenBot)
    
    #Obtenemos los usuarios autirozados
    usuarios= users.split(', ')
    # Generamos la hora de inicio del sistema
    hora=time.strftime("%H:%M:%S")

    return tokenBot, bot, usuarios, persianas, luces, calderas, rutaCred, rutaAuto, hora, pwdBot


tokenBot, bot, usuarios, persianas, luces, calderas, rutaCred, rutaAuto, hora, pwdBot = configBot()

# Listener recibira los mensajes que envian los usuarios.
def listener(messages):
    """
    Cuando lleguen nuevos mensajes, TeleBot llamara a esta funcion.
    Además, nos mostrará los mensajes recibidos en la consola (mientras no se lance en bg)
    """
    for m in messages:
        if m.content_type == 'text': #Comprueba si el mensaje es de tipo texto.
            # Imprime en la consola el mensaje recibido del usuario.
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
            #file_put_contents("registro_de_actualizaciones.log", $fecha.' - '.$request, FILE_APPEND);

#Lanzamos el listener 
bot.set_update_listener(listener)

# Comprueba si el usuario que nos escribe est'á en la lista de usuarios admitidos
def compruebaUsuario(message):
    # Filtramos por usuarios
    chatId = message.chat.id
    nombreUsuario = message.chat.first_name
    if str(chatId) in usuarios:
        #mensajeBienvenida = "Bienvenido, {nombre}. Selecciona una opción"
        #bot.send_message(chat_Id, mensajeElse.format(mensajeBienvenida=nombreUsuario))
        return 1
    else:
        mensajeElse = "Hola {nombre}, este bot funciona con invitación."
        bot.send_message(chatId, mensajeElse.format(nombre=nombreUsuario))
        sugerenciaElse = "Facilita tu Id: {chatId} al administrador para acceder."
        bot.send_message(chatId, sugerenciaElse.format(chatId=chatId))
        return 0
 
# Ayuda
@bot.message_handler(commands=['ayuda'])
@bot.message_handler(func=lambda message: message.text == "a")
@bot.message_handler(func=lambda message: message.text == "A")
@bot.message_handler(func=lambda message: message.text == "ayuda")
@bot.message_handler(func=lambda message: message.text == "Ayuda")
def command_help(m):  # Muestra al nuevo usuario el menú de ayuda
    if (compruebaUsuario(m)):
        chatId = m.chat.id
        #Crea una variable con el comando de ayuda completo
        help_text = "Los comandos disponibles son: \n\n"
        for key in commands:
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"
        bot.send_message(chatId, help_text) #Envia el mensaje de ayuda
 
# Reinicia Raspberry PI
@bot.message_handler(commands=['reiniciar'])
@bot.message_handler(func=lambda message: message.text == "reiniciar")
@bot.message_handler(func=lambda message: message.text == "Reiniciar")
def command_long_text(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        bot.send_message(usuario, "Reiniciando Raspberry PI...")
        time.sleep(3)
        os.system("sudo reboot")

# Apaga Raspberry PI
@bot.message_handler(commands=['apagar'])
@bot.message_handler(func=lambda message: message.text == "Apagar")
@bot.message_handler(func=lambda message: message.text == "apagar")
def command_long_text(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        bot.send_message(usuario, "Apagando Raspberry PI...")
        time.sleep(3)
        os.system("sudo shutdown -h now")

# Subir y Bajar persianas
@bot.message_handler(commands=['bajar'])
@bot.message_handler(commands=['subir'])
@bot.message_handler(commands=['parar'])
def command_long_text(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        try:
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

# Listado de temperaturas por horas (mañana)
@bot.message_handler(commands=['temp'])
@bot.message_handler(func=lambda message: message.text == "t")
@bot.message_handler(func=lambda message: message.text == "T")
def command_long_text(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        try:
            #Leemos información del archivo
            f = open(rutaAuto+"log.cron", "r")
            data = f.read()
            f.close()

            bot.send_chat_action(usuario, 'typing')
            time.sleep(1)

            #Obtenemos la primera línea aunque se puede cambiar a la segunda...
            matrix1 = data.split('\n')
            bot.send_message(usuario, "Las temperaturas por hora son:")

            ss = str(int(matrix1[4].split(" ")[2].split(":")[0]))
            ll = matrix1[5].split(" ")[2].split(":")[0]
            bb = matrix1[6].split(" ")[2].split(":")[0]
           
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
                if ((i >=20) and (i<34)):
                    compilado += str("\n|   ")+matrix1[i].split(", ")[0][1:]
                    if len(matrix1[i].split(", ")[1][:-1])==3:
                        compilado += str("   |  ")+matrix1[i].split(", ")[1][:-1]+str(" ºC   |")                    
                    if len(matrix1[i].split(", ")[1][:-1])==4:
                        compilado += str("   |  ")+matrix1[i].split(", ")[1][:-1]+str(" ºC  |")
                    if len(matrix1[i].split(", ")[1][:-1])==5:
                        compilado += str("   |  ")+matrix1[i].split(", ")[1][:-1]+str(" ºC |")
                    if (matrix1[i].split(", ")[0][1:]==bb):
                        compilado += str("&#128161;&#127770;")+str(matrix1[5].split(" ")[2][:-3])
            #print("-->")
            #print(compilado)
            bot.send_message(usuario, text='<pre><code class="language-python">'+compilado+'</code></pre>', parse_mode=ParseMode.HTML)
            
        except:
            bot.send_message(usuario, "Error en la lectura del archivo")

# Cambio de hora mínima de subida de persianas
@bot.message_handler(commands=['cambiar'])
def command_long_text(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        # Obtenemos la 'última imagen dentro de la ruta de imágenes
        try:
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

# Diagrama de temperaturas (enviar imagen)
@bot.message_handler(commands=['d'])
@bot.message_handler(func=lambda message: message.text == "d")
@bot.message_handler(func=lambda message: message.text == "D")
def command_long_text(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        # Obtenemos la 'última imagen dentro de la ruta de imágenes
        try:    
            pwdImagenes = rutaAuto+"diagramas/"
            os.chdir(pwdImagenes)
            result = os.popen('ls -r').read()
            imagenPorDefecto=((result.split("\n"))[0])
            os.chdir(pwdBot)
            
            imagenDefecto=(str(pwdImagenes)+str(imagenPorDefecto))
        
            print(len(m.text[len("/d"):].split()))
            #d = os.popen(m.text[len("/d"):])
            if ((len(m.text[len("/d "):])) > 0):
                nombre= str(m.text[len("/d "):])
                imagenUsuario=(str(pwdImagenes)+str(nombre)+".png")
                print(imagenUsuario)
                bot.send_photo(usuario,photo=open(imagenUsuario, 'rb'))
            else:
                bot.send_photo(usuario,photo=open(imagenDefecto, 'rb'))
        except:
            pwdImagenes = rutaAuto+"diagramas/"
            os.chdir(pwdImagenes)
            bot.send_message(usuario, "Error. Prueba con alguna de estas con formato AAAA-MM-DD:\n")
            result = os.popen('ls -r | rev | cut -f 2- -d "." | rev').read()
            cosa=((result.split("\n")))
            
            #Últimas 10 imágenes para no recargar la salida
            for i in range(len(cosa)):
                while i<10:
                    bot.send_message(usuario, cosa[i])
                    print(cosa[i])
                    i=i+1

# Lanzar Todo el proceso y generar nuevo CRON
@bot.message_handler(commands=['generar'])
@bot.message_handler(func=lambda message: message.text == "g")
@bot.message_handler(func=lambda message: message.text == "g")
def command_long_text(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        # Obtenemos la 'última imagen dentro de la ruta de imágenes
        try:
            #bot.send_message(usuario, "Comenzamos el proceso...")
            p = os.popen("bash " +rutaAuto+"LanzaTodoElProceso.sh")
            #bot.send_message(usuario, "Terminamos el proceso ^^")

            #Leemos información del archivo        
            f = open(rutaAuto+"log.cron", "r")
            data = f.read()
            f.close()
        
            #Obtenemos la primera línea aunque se puede cambiar a la segunda...
            matrix1 = data.split('\n')
            bot.send_message(usuario, "Datos obtenidos el "+matrix1[0]+" a las "+matrix1[1].split(' ')[3])
        except:
            bot.send_message(usuario, "Error!\n")

#Información de obtención de datos (Última línea del log)
@bot.message_handler(commands=['datos'])
@bot.message_handler(func=lambda message: message.text == "Datos")
@bot.message_handler(func=lambda message: message.text == "datos")
def command_text_hi(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
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
            mm += matrix1[4].split(" ")[0]+str("  | ")+matrix1[4].split(" ")[2]+ str(" | &#127774; \n|")
            mm += matrix1[5].split(" ")[0]+str("    | ")+matrix1[5].split(" ")[2]+ str(" | &#128161; \n|")
            mm += matrix1[6].split(" ")[0]+str(" | ")+matrix1[6].split(" ")[2]+ str(" | &#127770; \n</pre>")

            bot.send_message(usuario, text=mm, parse_mode=ParseMode.HTML)
           
        except:
            bot.send_message(usuario, "Error en la lectura del archivo")

# Hora mínima de subida de las persianas
@bot.message_handler(commands=['hora'])
@bot.message_handler(func=lambda message: message.text == "H")
@bot.message_handler(func=lambda message: message.text == "h")
@bot.message_handler(func=lambda message: message.text == "hora")
@bot.message_handler(func=lambda message: message.text == "Hora")
def command_text_hi(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        try:
            #Leemos información del archivo        
            f = open(rutaAuto+"HoraMinima")
            data = f.read()
            f.close()
           
            bot.send_chat_action(usuario, 'typing')
            time.sleep(1)

            #Obtenemos la primera línea aunque se puede cambiar a la segunda...
            matrix1 = data.split('\n')
            mm=matrix1[:1][0]
            bot.send_message(usuario, "Las persianas se subirán como pronto a las *"+mm[:-3]+"*",parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.send_message(usuario, "Error al obtener la hora")

# INFO TEMP
def temp():
    p = os.popen('cat /sys/class/thermal/thermal_zone0/temp')
    result = p.read()
    temp = int(result)/1000
    return temp

# INFO HD
def diskSpace():
    p = os.popen("df")
    i = 0
    while 1:
        i += 1
        line = p.readline()
        if i == 1:
            primero=(line.split()[1:2])+(line.split()[4:7])
        if i == 2:
            segundo=(line.split()[1:5])
            result = list(zip(primero, segundo))
            return(result)

# INFO RAM
def ramInfo():
    p = os.popen('vmstat -s -S M | grep memory')
    result = p.read()
    return result

# Información de nuestra Raspberry Pi
@bot.message_handler(commands=['info'])
@bot.message_handler(func=lambda message: message.text == "info")
@bot.message_handler(func=lambda message: message.text == "i")
@bot.message_handler(func=lambda message: message.text == "I")
@bot.message_handler(func=lambda message: message.text == "Info")
def command_long_text(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        try:
            result = ramInfo()
            primero=diskSpace()
            temperatura=temp()
            
            bot.send_message(usuario, text="*Espacio en disco*:\n",parse_mode=telegram.ParseMode.MARKDOWN)
            #tab = '\t'
            mm=""
            mm += str("| B")+str(primero[0][0][1:]) + str("    | ") + str(primero[0][1]) + str(" |\n")
            mm += str("| ")+str(primero[1][0][:-1]) + str("      | ") + str(primero[1][1]) + str("  |\n")
            mm += str("| ")+str(primero[2][0][:-1]) + str(" | ") + str(primero[2][1]) + str(" |\n")
            mm += str("| ")+str(primero[3][0]) + str("       | ") + str(primero[3][1]) + str("       |\n")

            bot.send_message(usuario, text='<pre><code class="language-python">'+mm+'</code></pre>', parse_mode='html')

            # Preparamos los datos de la RAM:
            pp=""
            for i in result:
                pp += str(i)
            ll=" ".join(pp.split())
            oo=ll.split("M")
            yep=[]
            for o in oo:
                yep.append(o.split(" "))
            
            mm = ""
            mm += str("| ")+str(yep[1][1])+str(" ")+str(yep[1][2])+str("    | ") +str(yep[0][0]) + str(" Mb |\n")
            mm += str("| ")+str(yep[2][1])+str(" ")+str(yep[2][2])+str("     | ") +str(yep[1][3]) + str(" Mb |\n")
            mm += str("| ")+str(yep[3][1])+str(" ")+str(yep[3][2])+str("   | ") +str(yep[2][3]) + str(" Mb |\n")
            mm += str("| ")+str(yep[4][1])+str(" ")+str(yep[4][2])+str(" | ") +str(yep[3][3]) + str(" Mb |\n")

            bot.send_message(usuario, text="*Estado RAM*:\n",parse_mode=telegram.ParseMode.MARKDOWN)
            bot.send_message(usuario, text='<pre><code class="language-python">'+mm+'</code></pre>', parse_mode='html')

            bot.send_message(usuario, text="*Temperatura CPU*: "+str(temperatura)+"ºC\n",parse_mode=telegram.ParseMode.MARKDOWN)

            fecha = str(datetime.datetime.today())
            bot.send_message(usuario, text="*Fecha: *"+str(fecha[:-7]),parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.send_message(usuario, text="*Hay algún problema en la obtención de datos.*",parse_mode=telegram.ParseMode.MARKDOWN)


@bot.message_handler(func=lambda message: message.text == "x")
def command_long_text(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        pass
    
    
# Control para cualquier otro texto.
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    usuario = m.chat.id
    nombreUsuario = m.chat.first_name
    if (compruebaUsuario(m)):
        # Esta es la respuesta estándar a un mensaje normal.
        bot.send_message(m.chat.id, "No te entiendo, prueba con /ayuda")
    else:
         mensajeElse = "Hola {nombre}, este bot funciona con invitación."
         bot.send_message(usuario, mensajeElse.format(nombre=nombreUsuario))
         mensajeElse = "Facilita tu id: {chat_Id} al administrador para acceder."
         bot.send_message(usuario, mensajeElse.format(chat_Id=usuario))

bot.polling() # Con esto, le decimos al bot que siga funcionando incluso si encuentra algun fallo.

