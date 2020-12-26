def info(m, bot):
    try:
        import os, obtencionDatos, time, datetime
        from telegram import ParseMode
        
        usuario = m.chat.id
        tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()
        
        result = ramInfo()
        primero=diskSpace()
        temperatura=temp()
        
        m1='<b>Espacio en disco:</b>\n<pre><code class="language-python">'
        m1 += str("| B")+str(primero[0][0][1:]) + str("    | ") + str(primero[0][1]) + str(" |\n")
        m1 += str("| ")+str(primero[1][0][:-1]) + str("      | ") + str(primero[1][1]) + str("  |\n")
        m1 += str("| ")+str(primero[2][0][:-1]) + str(" | ") + str(primero[2][1]) + str(" |\n")
        m1 += str("| ")+str(primero[3][0]) + str("       | ") + str(primero[3][1]) + str("       |\n")
        m1 += "</code></pre>"

        # Preparamos los datos de la RAM:
        pp=""
        for i in result:
            pp += str(i)
        ll=" ".join(pp.split())
        oo=ll.split("M")
        yep=[]
        for o in oo:
            yep.append(o.split(" "))
        
        m1 += '\n<b>Estado RAM:</b>\n<pre><code class="language-python">'
        m1 += str("| ")+str(yep[1][1])+str(" ")+str(yep[1][2])+str("    | ") +str(yep[0][0]) + str(" Mb |\n")
        m1 += str("| ")+str(yep[2][1])+str(" ")+str(yep[2][2])+str("     | ") +str(yep[1][3]) + str(" Mb |\n")
        m1 += str("| ")+str(yep[3][1])+str(" ")+str(yep[3][2])+str("   | ") +str(yep[2][3]) + str(" Mb |\n")
        m1 += str("| ")+str(yep[4][1])+str(" ")+str(yep[4][2])+str(" | ") +str(yep[3][3]) + str(" Mb |\n")
        m1 += "</code></pre>"
        
        bot.send_message(usuario, text=m1, parse_mode='html')

        m2="*Temperatura CPU: *"+ str(temperatura)[:5]+"ºC\n\n"+"*Fecha: *"+ str(datetime.datetime.today())[:-10]+"h"
        
        bot.send_message(usuario, m2, parse_mode=ParseMode.MARKDOWN)

    except:
        bot.send_message(usuario, text="*Hay algún problema en la obtención de datos.*",parse_mode=telegram.ParseMode.MARKDOWN)
        print("error general")
        
# INFO TEMP
def temp():
    import os
    p = os.popen('cat /sys/class/thermal/thermal_zone0/temp')
    result = p.read()
    temp = int(result)/1000
    return temp

# INFO HD
def diskSpace():
    import os
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
    import os
    p = os.popen('vmstat -s -S M | grep memory')
    result = p.read()
    return result