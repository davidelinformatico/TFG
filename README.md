<img width="300" src="https://www.raspberrypi.org/app/uploads/2017/06/Powered-by-Raspberry-Pi-Logo_Outline-Colour-Screen-500x153.png" align="right" />

# Sistema Domótico Inteligente
> Proyecto domótico autónomo que controla persianas, calefacción y luces.

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=davidelinformatico_TFG&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=davidelinformatico_TFG) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=davidelinformatico_TFG&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=davidelinformatico_TFG) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=davidelinformatico_TFG&metric=security_rating)](https://sonarcloud.io/dashboard?id=davidelinformatico_TFG) 

## Objeto
En proyecto se pretende crear un sistema domótico automatizado que nos permite aumentar la sensación de confort y bienestar dentro de nuestros domicilios.
Nuestro simulador de presencia funciona de forma autónoma subiendo y bajando persianas, así como encendiendo y apagando luces, desde una máquina RaspberryPi mediante relés. De esta forma la vivienda parece estar ocupada de forma que ahuyentamos a potenciales delincuentes.

## Puntos básicos
Para ello se han alcanzado algunos objetivos mínimos:
*	El sistema domótico funciona de forma autónoma.
*	Es un proyecto de bajo coste y asequible.
*	Corre sobre un Sistema Operativo GNU (Raspbian Os).
*	Posibilidad de interacción multiplataforma.
*	Fácilmente escalable.
*	Consigue un ahorro energético real.

## Funcionamiento del código

El código se divide en tres partes:
1.	Recopilación de datos y automatización del sistema.
2.  Control de los periféricos.
3.	Interacción a través del bot.

Las funciones que nos ofrecen, ordenados cronológicamente son:
1. Obtención de datos meteorológicos, geográficos y astronómicos de APIs externas.
2. Los datos son procesados y se almacenan en el equipo.
3. Se genera una automatización diaria ajustando los parámetros según la información recogida.
4. Los datos pueden ser entregados mediante un bot de Telegram.
5. Desde el bot podemos cambiar la configuración de nuestro sistema automatizado, entre otras opciones.
6. También podemos controlar el sistema de persianas motorizadas a placer.

## Escalabilidad
Además, este sistema domótico es fácilmente escalable con sistemas de acceso a la vivienda, telefonía IP, música, calefacción, telefonillo IP, etc.

## Calidad del código comprobado con SonarCLoud
La calidad del código se ha comprobado mediante la plataforma SonarCloud, accesible desde este logo:
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=davidelinformatico_TFG&metric=alert_status)](https://sonarcloud.io/dashboard?id=davidelinformatico_TFG)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=davidelinformatico_TFG&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=davidelinformatico_TFG) [![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=davidelinformatico_TFG&metric=ncloc)](https://sonarcloud.io/dashboard?id=davidelinformatico_TFG)  [![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=davidelinformatico_TFG&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=davidelinformatico_TFG)

## Licencia
El proyecto se ha desarrollado bajo las siguientes licencias:  
Código Fuente:	GPL3  
Documentación:	CC-BY-SA-3.0  
Imágenes:		CC-BY-SA-3.0  

[![License: CC BY-SA 3.0](https://licensebuttons.net/l/by-sa/3.0/es/88x31.png)](https://creativecommons.org/licenses/by-sa/3.0/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) 

## Donativo al desarrollo
[
  ![Donate with PayPal]
  (https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png)
]
(https://www.paypal.com/donate?hosted_button_id=JMTPACKMU58PA)
