
def obtencionDatos():
    # Importamos numpy y random para obtener números aleatorios
    import telebot, logging, subprocess, telegram, math, os, random
    from telebot import types
    import time, requests, datetime, sys

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
    
    # Leemos el archivo
    f = open(rutaCred+"config2.bot")
    data = f.read()
    f.close()

    matrizBruta = data.split('\n')

    tokenBot=matrizBruta[1]
    users=matrizBruta[4]
    climacellKey=matrizBruta[7]
    weatherApiKey=matrizBruta[10]
    terminaKeys=14

    lineasPersianas = matrizBruta[terminaKeys]
    empiezanLuces = 4+int(lineasPersianas)+int(terminaKeys)
    lineasLuces = matrizBruta[empiezanLuces]
    terminanLuces = int(empiezanLuces)+int(lineasLuces)
    caldera=matrizBruta[int(terminanLuces)+4]

    persianas=[]
    for i in range(int(terminaKeys)+1,terminaKeys+int(lineasPersianas)+1):
        persianas.append(str(matrizBruta[i]).split(" "))

    luces=[]
    for i in range(empiezanLuces+1,terminanLuces+1):
        luces.append(str(matrizBruta[i]).split(" "))

    calderas=[]
    for i in range(terminanLuces+5,terminanLuces+6):
        calderas.append(str(matrizBruta[i]).split(" "))

    return tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto






