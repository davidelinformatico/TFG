# Importamos numpy y random para obtener números aleatorios
import numpy as np
import random
import math
import os

#------------------------------------------------------------------------------------
# # # # # # # # # # # # # # # # CONFIGURACIONES # # # # # # # # # # # # # # # # # # # 
#------------------------------------------------------------------------------------

# Si quieres cambiar el tiempo entre accionar dos elementos debes cambiarlo aquí, 
# en los <<tiempos>>, tiempoBajada, tiempoSubida y tiempoLuces.
# La caldera no dispone de tiempo de seguridad porque se contempla sólo una caldera.

# Generamos el tiempo de espera entre eventos
tiempoBajada = str(15) # Entre persianas subiendo.
tiempoSubida = str(10) # Entre persianas bajando.
tiempoLuces = str(15)  # Entre luces (apagando y encendiendo)

#------------------------------------------------------------------------------------
# # # # # # # # # # # NO DEBES MANIPULAR NADA MÁS EN EL CÓDIGO  # # # # # # # # # # # 
#------------------------------------------------------------------------------------

# Leemos el archivo
try:
    f = open("config2.bot")
    data = f.read()
    f.close()
except Exception as e:
    print(e)
   
   
matrizBruta = data.split('\n')
#matrizBuena = matrizBruta.split(',')
# matrizSucia = np.loadtxt(matrizBruta, dtype=int)

tokenBot=matrizBruta[1]
usuarios=matrizBruta[4]
climacellKey=matrizBruta[7]
weatherApiKey=matrizBruta[10]
terminaKeys=14

lineasPersianas = matrizBruta[terminaKeys]
empiezanLuces = 4+int(lineasPersianas)+int(terminaKeys)
lineasLuces = matrizBruta[empiezanLuces]
terminanLuces = int(empiezanLuces)+int(lineasLuces)
caldera=matrizBruta[int(terminanLuces)+4]

print("Tenemos "+str(lineasPersianas)+" persianas")
print("Tenemos "+str(lineasLuces)+" luces")
print("Tenemos "+str(caldera)+" calderas")

persianas=[]
for i in range(int(terminaKeys)+1,terminaKeys+int(lineasPersianas)+1):
    persianas.append(str(matrizBruta[i]).split(" "))

luces=[]
for i in range(empiezanLuces+1,terminanLuces+1):
    luces.append(str(matrizBruta[i]).split(" "))

calderas=[]
for i in range(terminanLuces+5,terminanLuces+6):
    calderas.append(str(matrizBruta[i]).split(" "))

#Generamos la matriz con la que trabajaremos
if int(lineasPersianas)>0 : 

    # Generamos las listas de control de las persianas
    nombresPersianas=[]
    pinesSubida=[]
    pinesBajada=[]

    for i in range(int(lineasPersianas)):
        for j in range(3):
            if j==0:
                nombresPersianas.append(persianas[i][j])
            if j==1:
                pinesSubida.append(persianas[i][j])
            if j==2:
                pinesBajada.append(persianas[i][j])
                
    
#     print(nombresPersianas, pinesSubida, pinesBajada)
    
    salidaPersianas = subidas = bajadas = pinesUp = pinesDown = ""
    
    # Tiramos todos los GPIO
    for i in pinesSubida:
        pinesUp += ("\ngpio -g mode "+str(i)+" in")
    for i in pinesBajada:
        pinesDown += ("\ngpio -g mode "+str(i)+" in")
    print(" ")
    # Todos los GPIO están caidos
    
    # Subimos las persianas 
    for i in range(len(pinesSubida)):
        subidas += ("\n# Subimos las persianas de "+str(nombresPersianas[i]))
        subidas += ("\ngpio -g mode "+str(pinesSubida[i]+" out"))
        subidas += ("\nsleep "+ str(tiempoSubida))
        subidas += ("\ngpio -g mode "+str(pinesSubida[i]+" in"))
        subidas += ("\n")
        
    # Bajamos las persianas 
    for i in range(len(pinesBajada)):
        bajadas += ("\n# Bajamos las persianas de "+str(nombresPersianas[i]))
        bajadas += ("\ngpio -g mode "+str(pinesBajada[i]+" out"))
        bajadas += ("\nsleep "+ str(tiempoBajada))
        bajadas += ("\ngpio -g mode "+str(pinesBajada[i]+" in"))
        bajadas += ("\n")
    
    # Tiramos los GPIO de las persianas
    for i in range(len(pinesBajada)):
        salidaPersianas += ("\n# Tiramos los GPIO  de - "+str(nombresPersianas[i]))
        salidaPersianas += ("\ngpio -g mode "+str(pinesSubida[i]+" in"))
        salidaPersianas += ("\ngpio -g mode "+str(pinesBajada[i]+" in"))
        #salidaPersianas += ("\n")

# Grabamos los archivos
'''
Subir.sh        : Sube las persianas
Bajar.sh        : Baja las persianas
'''

try:
    # Volcamos los datos al archivo de Información recabada
    file = open ('Subir.sh','w')
    file.write(salidaPersianas+ os.linesep)
    file.write(subidas+ os.linesep)
    file.write(salidaPersianas+ os.linesep)
    file.close()
    
    file = open ('Bajar.sh','w')
    file.write(salidaPersianas+ os.linesep)
    file.write(bajadas+ os.linesep)
    file.write(salidaPersianas+ os.linesep)
    file.close()
except Exception as e:
    print(e)

# Generamos una matriz  de enteros con los valores que recibimos
if int(lineasLuces)>0:

    # Generamos los arrays de control de las luces
    nombresLuces=[]
    pinesControl=[]

    for i in range(int(lineasLuces)):
        for j in range(2):
            if j==0:
                nombresLuces.append(luces[i][j])
            if j==1:
                pinesControl.append(luces[i][j])
                
    lucesOn = lucesOff = lucesDown = ""
    # Encendemos las luces
    for i in range(len(pinesControl)):
        lucesOn += ("\n# Encendemos la luz de "+str(nombresLuces[i]))
        lucesOn += ("\ngpio -g mode "+str(pinesControl[i]+" out"))
        lucesOn += ("\nsleep " + tiempoLuces)
        lucesOn += ("\n")
    
    # Apagamos las luces
    for i in range(len(pinesControl)):
        lucesOff += ("\n# Encendemos la luz de "+str(nombresLuces[i]))
        lucesOff += ("\ngpio -g mode "+str(pinesControl[i]+" in"))
        lucesOff += ("\nsleep " + tiempoLuces)
        lucesOff += ("\n")
        
    # Tiramos los GPIO de las luces
    for i in range(len(pinesControl)):
        lucesDown += ("\n# Tiramos el GPIO de - "+str(nombresLuces[i]))
        lucesDown += ("\ngpio -g mode "+str(pinesControl[i]+" in"))
        lucesDown += ("\n")



# Grabamos los archivos
'''
LucesOff.sh     : Apaga las luces
LucesOn.sh      : Enciende las luces
'''

try:
    # Volcamos los datos al archivo de Información recabada
    file = open ('LucesOn.sh','w')
    file.write(lucesDown+ os.linesep)
    file.write(lucesOn+ os.linesep)
    file.write(lucesDown+ os.linesep)
    file.close()
    
    file = open ('LucesOff.sh','w')
    file.write(lucesDown+ os.linesep)
    file.write(lucesOff+ os.linesep)
    file.write(lucesDown+ os.linesep)
    file.close()
except Exception as e:
    print(e)

# Generamos una matriz  de enteros con los valores que recibimos
if int(caldera)>0 : 

    # Generamos los arrays de control de las luces
    nombresUbicaciones=[]
    pinesControl=[]

    for i in range(int(caldera)):
        for j in range(2):
            if j==0:
                nombresUbicaciones.append(calderas[i][j])
            if j==1:
                pinesControl.append(calderas[i][j])
    
    
    calderaOn = calderaOff = calderaDown = ""
    
    # Encendemos las calderas
    for i in range(len(pinesControl)):
        calderaOn += ("\n# Encendemos la caldera de "+str(nombresUbicaciones[i]))
        calderaOn += ("\ngpio -g mode "+str(pinesControl[i]+" out"))
        calderaOn += ("\n")
    
    # Apagamos las calderas
    for i in range(len(pinesControl)):
        calderaOff += ("\n# Encendemos la caldera de "+str(nombresUbicaciones[i]))
        calderaOff += ("\ngpio -g mode "+str(pinesControl[i]+" in"))
        calderaOff += ("\n")

    # Tiramos los GPIO de las persianas
    for i in range(len(pinesControl)):
        calderaDown += ("\n# Tiramos todos los GPIO - "+str(nombresUbicaciones[i]))
        calderaDown += ("\ngpio -g mode "+str(pinesControl[i]+" in"))
        calderaDown += ("\n")



# Grabamos los archivos
'''
ApagarCaldera.sh: Apaga la caldera
EncenderCaldera : Enciende la caldera
'''

try:
    # Volcamos los datos al archivo de Información recabada
    file = open ('EncenderCaldera.sh','w')
    file.write(calderaDown+ os.linesep)
    file.write(calderaOn+ os.linesep)
    file.write(calderaDown+ os.linesep)
    file.close()
    
    file = open ('ApagarCaldera.sh','w')
    file.write(calderaDown+ os.linesep)
    file.write(calderaOff+ os.linesep)
    file.write(calderaDown+ os.linesep)
    file.close()
except Exception as e:
    print(e)

















