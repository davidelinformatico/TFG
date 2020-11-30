
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

    return tokenBot, bot, usuarios, hora


tokenBot, bot, usuarios, hora = configBot()
    
updater = Updater(token=tokenBot, use_context=True)
dispatcher = updater.dispatcher

# Funciones:
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Dime qué quieres hacer")

    keyboard = [
        [InlineKeyboardButton("Subir Persianas", callback_data='SubirPersianas')],
        [InlineKeyboardButton("Bajar Persianas", callback_data='BajarPersianas')],
        [InlineKeyboardButton("Apagar Sistema Domótico", callback_data='Apagar')],
        [InlineKeyboardButton("Reiniciar Sistema Domótico", callback_data='Reiniciar')],
        [InlineKeyboardButton("Lista de Temperaturas", callback_data='Listado')],
        [InlineKeyboardButton("Diagrama de Temperaturas", callback_data='Diagrama')],
        [InlineKeyboardButton("Reiniciar Sistema Domótico", callback_data='Reiniciar')],
        [InlineKeyboardButton("Lista de Temperaturas Mañana", callback_data='ListadoMaana')],
        [InlineKeyboardButton("Diagrama de Temperaturas Mañana", callback_data='DiagramaManana')],
                ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Selecciona una opción:', reply_markup=reply_markup)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Comando desconocido...")



def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

# Lanzador o Negociador
start_handler = CommandHandler('help', help)
dispatcher.add_handler(start_handler)


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

#menu_handler = CommandHandler('menu', menu)
#dispatcher.add_handler(CallbackQueryHandler(button))


updater.start_polling()





























