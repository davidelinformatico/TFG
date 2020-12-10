import os

ruta=os.getcwd().split('/')
print(ruta)

salida=""
for i in range(len(ruta)-3):
    salida=str(salida)+"/"+str(ruta[i])

ruta=salida[1:]+str("/")

print(ruta)