import telebot, logging, subprocess, telegram
from telebot import types
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import time, requests, os, datetime, sys


# Registro de eventos
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('SDI_domo.log')

#Diccionario con los comandos disponibles en el bot.
commands = {
             'ayuda': 'Muestra información sobre los comandos',
             #'e': 'Ejecuta un comando',
             'subir': 'Subir persianas',
             'bajar': 'Bajar persianas',
             'temperaturas': 'Listado de temperaturas',
             'd': 'Diagrama de temperaturas',
             'cambiar': 'Cambiar hora subida',
             'apagar': ' Apagar sistema domótico',
             'reiniciar': 'Reinicia la Raspberry PI',
             'info': 'Información de la RaspberryPi',
             'datos': 'Hora de recopilación de datos',
             'hora': 'Hora a la que suben las persianas',
             'generar': 'Genera los archivos de control'
            }

# Configuración básica de nuestro Bot
def configBot():
    # Leemos el archivo
    f = open("./../../../credentials/config.bot")
    data = f.read()
    f.close()
    
    # Preparamos los datos cortando por los saltos de línea
    datos = data.split('\n')
    
    #Obtenemos el Token
    tokenBot = str(datos[1])
    bot = telebot.TeleBot(tokenBot)
    
    #Obtenemos los usuarios autirozados
    usuarios= datos[4].split(', ')
    # Generamos la hora de inicio del sistema
    hora=time.strftime("%H:%M:%S")
    result = os.popen('pwd').read()
    pwdBot=result.split("\n")[0]
    
    return tokenBot, bot, usuarios, hora, pwdBot


tokenBot, bot, usuarios, hora, pwdBot = configBot()


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
         
# Ejecuta un comando
#@bot.message_handler(commands=['e'])
#@bot.message_handler(func=lambda message: message.text == "e")
#@bot.message_handler(func=lambda message: message.text == "E")
#def command_long_text(m):
#    usuario = m.chat.id
#    if (compruebaUsuario(m)):
#        try:
#            if (len(m.text[len("/e"):].split())) < 1:
#                bot.send_message(usuario, "Debes introducir,al menos, un comando...")
#            else:
#                bot.send_message(usuario, "Ejecutando: "+m.text[len("/e"):])
#                bot.send_chat_action(usuario, 'typing') 
#                time.sleep(2)
#                f = os.popen(m.text[len("/e"):])
#                result = f.read()
#                bot.send_message(usuario, "Resultado:\n"+result)
#        except:
#            bot.send_message(usuario, "No es un comando válido...")


# Subir persianas
@bot.message_handler(commands=['subir'])
@bot.message_handler(func=lambda message: message.text == "s")
@bot.message_handler(func=lambda message: message.text == "S")
def command_long_text(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        bot.send_message(usuario, "Subiendo persianas... ")

        bot.send_message(usuario, "La persiana ha terminado de subir ^^")

# Bajar persianas
@bot.message_handler(commands=['bajar'])
@bot.message_handler(func=lambda message: message.text == "b")
@bot.message_handler(func=lambda message: message.text == "B")
def command_long_text(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        bot.send_message(usuario, "Bajando persianas... ")
        
        bot.send_message(usuario, "Las persianas han terminado de bajar.")
    

# Listado de temperaturas por horas (mañana)
@bot.message_handler(commands=['temperaturas'])
@bot.message_handler(func=lambda message: message.text == "t")
@bot.message_handler(func=lambda message: message.text == "T")
def command_long_text(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        try:
            #Leemos información del archivo        
            f = open("./../auto/log.cron", "r")
            data = f.read()
            f.close()
        
            bot.send_chat_action(usuario, 'typing')
            time.sleep(1)

            #Obtenemos la primera línea aunque se puede cambiar a la segunda...
            matrix1 = data.split('\n')

            bot.send_message(usuario, "Las temperaturas por hora son:")
            bot.send_message(usuario, "hr Temp")
            bot.send_message(usuario, "-- ---------")

            for i in range(len(matrix1)-1):
                if ((i >10) and (i<34)):
                    bot.send_message(usuario, matrix1[i].split(", ")[0][1:]+str(" ")+matrix1[i].split(", ")[1][:-1]+str("ºC"))

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
            f = open("./../auto/HoraMinima")
            horaAntigua = f.read()
            f.close()
            # Leemos la hora introducida por parámetro
            horaNueva=str((m.text[len("/cambiar"):].split())[0])
            if len(horaNueva)==8:
                f = open("./../auto/HoraMinima", "w")
                f.write(str(horaNueva))
                f.close()

                #Comprobamos el cambio de hora
                f = open("./../auto/HoraMinima")
                horaNueva = f.read()
                f.close()
                #Leemos hora a cambiar
                bot.send_message(usuario, "La hora ha cambiado de "+str(horaAntigua) + " a *"+str(horaNueva)+"*",parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.send_message(usuario, "Introduce el formato correcto: HH:MM:SS")    
        except:
            bot.send_message(usuario, "Error!\n")

# Cambio de hora mínima de subida de persianas
@bot.message_handler(commands=['cambiar'])
def command_long_text(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        # Obtenemos la 'última imagen dentro de la ruta de imágenes
        try:
            # Leemos hora antigua
            f = open("./../auto/HoraMinima")
            horaAntigua = f.read()
            f.close()
            # Leemos la hora introducida por parámetro
            horaNueva=str((m.text[len("/cambiar"):].split())[0])
            if len(horaNueva)==8:
                f = open("./../auto/HoraMinima", "w")
                f.write(str(horaNueva))
                f.close()

                #Comprobamos el cambio de hora
                f = open("./../auto/HoraMinima")
                horaNueva = f.read()
                f.close()
                #Leemos hora a cambiar
                bot.send_message(usuario, "La hora ha cambiado de "+str(horaAntigua) + " a *"+str(horaNueva)+"*",parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.send_message(usuario, "Introduce el formato correcto: HH:MM:SS")    
        except:
            bot.send_message(usuario, "Error!\n")


# Lanzar Todo el proceso y generar nuevo CRON
@bot.message_handler(commands=['generar'])
@bot.message_handler(func=lambda message: message.text == "g")
@bot.message_handler(func=lambda message: message.text == "g")
def command_long_text(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        # Obtenemos la 'última imagen dentro de la ruta de imágenes
        try:
            bot.send_message(usuario, "Comenzamos el proceso...")
            p = os.popen("bash ./../auto/LanzaTodoElProceso.sh")
            bot.send_message(usuario, "Terminamos el proceso ^^")

            #Leemos información del archivo        
            f = open("./../auto/log.cron", "r")
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
@bot.message_handler(func=lambda message: message.text == "x")
def command_text_hi(m):
    usuario = m.chat.id
    if (compruebaUsuario(m)):
        try:
            #Leemos información del archivo        
            f = open("./../auto/log.cron", "r")
            data = f.read()
            f.close()
        
            bot.send_chat_action(usuario, 'typing')
            time.sleep(1)

            #Obtenemos la primera línea aunque se puede cambiar a la segunda...
            matrix1 = data.split('\n')

            bot.send_message(usuario, "Datos obtenidos el "+matrix1[0]+" a las "+matrix1[1].split(' ')[3])
            bot.send_message(usuario, matrix1[4].split(" ")[0]+str(" ")+matrix1[4].split(" ")[2])
            bot.send_message(usuario, matrix1[5].split(" ")[0]+str(" ")+matrix1[5].split(" ")[2])
            bot.send_message(usuario, matrix1[6].split(" ")[0]+str(" ")+matrix1[6].split(" ")[2])
            #bot.send_message(usuario, "Las temperaturas por hora son:")
            #bot.send_message(usuario, "hr Temp")
            #bot.send_message(usuario, "-- ---------")
            #for i in range(len(matrix1)-1):
            #    if ((i >10) and (i<34)):
            #        bot.send_message(usuario, matrix1[i].split(", ")[0][1:]+str(" ")+matrix1[i].split(", ")[1][:-1]+str("ºC"))
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
            f = open("./../auto/HoraMinima")
            data = f.read()
            f.close()
           
            bot.send_chat_action(usuario, 'typing')
            time.sleep(1)

            #Obtenemos la primera línea aunque se puede cambiar a la segunda...
            matrix1 = data.split('\n')
            mm=matrix1[:1][0]
            bot.send_message(usuario, "Las persianas se subirán como pronto a las "+mm)
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
            tab = '\t'
            for i in primero:                
                bot.send_message(usuario, str(i[0]) + str(" > ") + str(i[1]) + str("\n"))
            bot.send_message(usuario, text="*Estado RAM*:\n"+result,parse_mode=telegram.ParseMode.MARKDOWN)
            bot.send_message(usuario, text="*Temperatura CPU*: "+str(temperatura)+"ºC\n",parse_mode=telegram.ParseMode.MARKDOWN)

            fecha = str(datetime.datetime.today())
            bot.send_message(usuario, text="*Fecha: *"+str(fecha),parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.send_message(usuario, text="*Hay algún problema en la obtención de datos.*",parse_mode=telegram.ParseMode.MARKDOWN)


# Control para cualquier otro texto.
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    usuario = m.chat.id
    nombreUsuario = m.chat.first_name
    if (compruebaUsuario(m)):
        # Esta es la respuesta estándar a un mensaje normal.
        bot.send_message(m.chat.id, "No te entiendo, prueba con /ayuda")
#     else:
#         mensajeElse = "Hola {nombre}, este bot funciona con invitación."
#         bot.send_message(usuario, mensajeElse.format(nombre=nombreUsuario))
#         mensajeElse = "Facilita tu id: {chat_Id} al administrador para acceder."
#         bot.send_message(usuario, mensajeElse.format(chat_Id=usuario))

bot.polling(none_stop=True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algun fallo.

