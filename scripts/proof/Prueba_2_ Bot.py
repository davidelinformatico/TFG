
from telebot import types
import time, requests, os, telebot, datetime, logging, traceback, sys
import numpy as np
from telegram.ext import Updater, InlineQueryHandler, MessageHandler, CallbackContext, CommandHandler
from telegram.ext import CallbackQueryHandler, Handler, Filters

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, InlineKeyboardButton, InlineKeyboardMarkup



def configBot():
    # Leemos el archivo
    f = open("config.bot")
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

    return bot, usuarios, hora


bot, usuarios, hora = configBot()
    
def compruebaUsuario(usuario):
        # Filtramos por usuarios
    if str(usuario) in usuarios:
      
        return 1
    else:
        return 0

@bot.message_handler(commands = ['start', "help"])
def enviarMensaje(message):

    # Obtenemos parámetros del remitente de la conversación
    chatId = message.chat.id
    nombreUsuario = message.chat.first_name

    # Filtramos por usuarios
    if compruebaUsuario(chatId):
        #correctoId = "Bienvenido {id}, tu credencial es correcta."
        #bot.send_message(chatId, correctoId.format(id=chatId))
        bot.send_message(chatId, "Bienvenido, tu credencial es correcta.")

        # Iniciamos el teclado
        markup = types.ReplyKeyboardMarkup()

        btn1 = types.KeyboardButton('/help')
        btn2 = types.KeyboardButton('Cambio de Hora')
        btn3 = types.KeyboardButton('Información Domótica')
        btn4 = types.KeyboardButton('Imagen Temperaturas')
        btn5 = types.KeyboardButton('Control Persianas')
        btn6 = types.KeyboardButton('Apagar Máquina')

        markup.row(btn1, btn2, btn3)
        markup.row(btn4, btn5, btn6)

        msg = bot.send_message(chatId,"Selecciona una tarea", reply_markup=markup)
        bot.register_next_step_handler(msg, cambioDeHora)

    else:
        # Mensaje general
        mensajeElse = "Hola {nombre}, este bot funciona con invitación."
        bot.send_message(chatId, mensajeElse.format(nombre=nombreUsuario))
        sugerenciaElse = "Facilita tu Id: {chatId} al administrador para acceder."
        bot.send_message(chatId, mensajeElse.format(chatId=chatId))

#@bot.message_handler(commands = ['/cambioDeHora'])
def cambioDeHora(message):
    #print(message)
    opcionSeleccionada = message.json['text']
    chatId = message.chat.id
    custom= types.ReplyKeyboardRemove()
    
    if (opcionSeleccionada=="Cambio de Hora"):
        bot.reply_to(message, "Introduce la hora")
        recibido = recogeMensaje()
        print(recibido)

def recogeMensaje(message):
    #print(message)
    return message

@bot.message_handler(func=lambda message: True)
def echo_all(mensaje):
    bot.reply_to(mensaje, "No entiendo tu mensaje, prueba otra vez.")


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()


bot.polling()
#updater.start_polling()




