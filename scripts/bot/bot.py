import telebot, logging, subprocess, telegram, os, time, requests, datetime, sys
from telebot import types
from telegram import ParseMode

import obtencionDatos, subirPararBajar, temperaturasManana, temperaturaCalefaccion, horaSubida, diagramaTemperaturas
import generador, datos, horaSubida, info


# Registro de eventos
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('SDI_domo.log')

#Diccionario con los comandos disponibles en el bot.
commands = {
             'ayuda': 'Muestra información sobre los comandos',
             'subir': 'Subir persianas',
             'bajar': 'Bajar persianas',
             'parar': 'Para las persianas',
             'temp': 'Listado de temperaturas',
             'd': 'Diagrama de temperaturas',
             'tempcal': 'Informa y cambia temperatura de calefacción',
             'datos': 'Hora de recopilación de datos',
             'hora': 'Informa o cambia hora de subida de las persianas',
             'generar': 'Genera los archivos de control',
             'info': 'Información de la RaspberryPi',
             'apagar': ' Apagar sistema domótico',
             'reiniciar': 'Reinicia la Raspberry PI'
            }

# Configuración básica de nuestro Bot
def configBot():
    #Calculamos ruta
    pwdBot=os.getcwd()

    tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()

    #Obtenemos el Token
    bot = telebot.TeleBot(tokenBot)
    
    #Obtenemos los usuarios autirozados
    usuarios= users.split(', ')
    # Generamos la hora de inicio del sistema
    hora=time.strftime("%H:%M:%S")
    
    for usuario in usuarios:
        bot.send_message(usuario, "Iniciando Sistema a las "+str(hora))

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
    if (compruebaUsuario(m)):
        subirPararBajar.controlPersianas(m, bot)
     

# Listado de temperaturas por horas (mañana)
@bot.message_handler(commands=['temp'])
@bot.message_handler(func=lambda message: message.text == "t")
@bot.message_handler(func=lambda message: message.text == "T")
def command_long_text(m):
    if (compruebaUsuario(m)):
        temperaturasManana.temperaturas(m , bot)


# Informa y cambia temperatura de calefacción
@bot.message_handler(commands=['tempcal'])
@bot.message_handler(func=lambda message: message.text == "tc")
@bot.message_handler(func=lambda message: message.text == "Tc")
def command_long_text(m):
    if (compruebaUsuario(m)):
        temperaturaCalefaccion.calefaccion(m, bot)


# Diagrama de temperaturas (enviar imagen)
@bot.message_handler(commands=['d'])
@bot.message_handler(func=lambda message: message.text == "d")
@bot.message_handler(func=lambda message: message.text == "D")
def command_long_text(m):
    if (compruebaUsuario(m)):
        diagramaTemperaturas.diagrama(m, bot, pwdBot)
        

# Lanzar Todo el proceso y generar nuevo CRON
@bot.message_handler(commands=['generar'])
@bot.message_handler(func=lambda message: message.text == "g")
@bot.message_handler(func=lambda message: message.text == "g")
def command_long_text(m):
    if (compruebaUsuario(m)):
        generador.generador(m, bot)
        

#Información de obtención de datos (Última línea del log)
@bot.message_handler(commands=['datos'])
@bot.message_handler(func=lambda message: message.text == "Datos")
@bot.message_handler(func=lambda message: message.text == "datos")
def command_text_hi(m):
    if (compruebaUsuario(m)):
        datos.datos(m, bot)
        
        
# Hora mínima de subida de las persianas
@bot.message_handler(commands=['hora'])
@bot.message_handler(func=lambda message: message.text == "H")
@bot.message_handler(func=lambda message: message.text == "h")
@bot.message_handler(func=lambda message: message.text == "hora")
@bot.message_handler(func=lambda message: message.text == "Hora")
def command_text_hi(m):
    if (compruebaUsuario(m)):
        horaSubida.horaSubida(m, bot)


# Información de nuestra Raspberry Pi
@bot.message_handler(commands=['info'])
@bot.message_handler(func=lambda message: message.text == "info")
@bot.message_handler(func=lambda message: message.text == "i")
@bot.message_handler(func=lambda message: message.text == "I")
@bot.message_handler(func=lambda message: message.text == "Info")
def command_long_text(m):
    if (compruebaUsuario(m)):
        info.info(m, bot)

    
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

