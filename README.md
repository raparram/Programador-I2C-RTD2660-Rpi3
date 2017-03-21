# PROGRAMADOR I2C PARA RTD2660 DESDE RASPBERRY PI
Este repositorio tiene como fin documentar y brindar las herramientas necesarias para programar cualquier tarjeta que use RTD2660 y una memoria flash para guardar el firmware. Se da prioridad a los drives PCB800099 y PCB800661. Para desarrollar esta guía con éxito se requiere haber realizado estos pasos previos:

* Activación del I2C de la Raspberry Pi. Para mayor información visitar: http://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/

* Instalación de *python-smbus* y *i2c-tools* en la Raspberry Pi. Los puede instalar desde consola con la siguiente línea:
                  
        sudo apt-get install -y python-smbus i2c-tools

## Como seleccionar el firmware
Si su tarjeta es PCB800099 o PCB800661 probablemente el firmware que busca esta en alguna de las carpetas adjuntas, en el caso contrario, la sugerencia es solicitarlo a su proveedor. Desafortunadamente no he encontrado el código fuente para generar el *firmware.bin*, si usted logra obtenerlo y hacerlo funcionar, por favor hágaselo saber al mundo.

Para elegir el firmware también hay que tener en cuenta la pantalla, específicamente 3 características: resolución, visualización de color y clase de señal de salida, la forma más efectiva para obtener esta información es por medio del datasheet de la misma.

### Ejemplo:
* Pantalla LTN133AT16: http://panelone.net/es/13-3-pulgadas/SAMSUNG_LTN133AT16-S01_13.3_pulgadas-datasheet
* Driver: PCB800661

Identificamos:
* Resolución: 1280x800
* Visualización de color: 262k (6-bits)
* Clase de señal: LVDS

Buscando en la capeta PCB800661 encontramos el firmware *PCB800661-LVDS1280X800-D6BIT-!HDMI.BIN*, en su nombre encontramos la tarjeta PCB800661, la clase de señal LVDS, la resolución 1280X800, y la visualización de color D6BIT.

## Conexión 
Para realizar la programación del firmware debe realizar la siguiente conexión según la tarjeta:

* PCB800661:

![Conexión PCB800661](http://fotos.subefotos.com/d37b84e64cd67339c8d47c0f1d33d8cao.jpg)

* PCB800099:

![Conexión PCB800099](https://fotos.subefotos.com/5064c26c82d775459a9efa73a730a35do.png)

Si su tarjeta no corresponde a las anteriores, busque un puerto de programación, por lo general es un conector Grove de 4 pines, como el observado en la tarjeta PCB800661, de los cuales dos pines son GND y los otros dos corresponden al I2C, SDA y SCL.

## Programación
Antes de la programación hay que garantizar la correcta conexión entre la tarjeta y la Raspberry Pi, para ello ejecute desde consola la siguiente línea:

        sudo i2cdetect -y 1
        
Lo que hace la Raspberry Pi 3 es escanear todas las direcciones posibles en búsqueda de dispositivos conectados por I2C, la respuesta común es 4 o 3 dispositivos, varia según la tarjeta, si obtiene un resultado sin ninguna dirección activa debe revisar la conexión. Por consola debe ver lo siguiente:

![Scanner I2C Rpi3](https://fotos.subefotos.com/6994d725f236ee50a16930f3206dc05co.png)

Para ejecutar el programador debe abrir una terminal o consola desde la carpeta del repositorio e ingresar esta línea:

        python prog.py /la_ubicacion_del_firmware/firmware.bin

El proceso de carga del firmware puede demorar varios minutos, es normal, para tener una clara visión de una programación exitosa se invita a ver el archivo *test_consola*. 

### Ejemplo:
Para obtener el repositorio y programar puede usar los siguientes comandos desde su Raspberry:

        git clone https://github.com/raparram/Programador-I2C-RTD2660-Rpi3.git
        cd Programador-I2C-RTD2660-Rpi3
        python prog.py /home/pi/Programador-I2C-RTD2660-Rpi3/PCB800661-LVDS1366X768-D6BIT.BIN
       
## Una programación no exitosa es una oportunidad de colaborar
Si la consola le informa *>>> Review wiki to add new flash chip !* o cualquier otro mensaje diferente a *Done* es una excelente oportunidad para colaborar en el proyecto. Lo primero que debe hacer es conseguir el firmware, si tiene algún firmware diferente a los aquí publicados por favor súbalo, la mejor manera de hacerlo es en una carpeta nombrada como la referencia de la tarjeta. Para continuar con el proceso debe identificar la memoria flash que implementa su driver, una buena pista es el Jedec ID informado por este código, con la referencia clara, se debe proceder a actualizar el arreglo de objetos *FlashDevices*, ubicado entre las líneas 32 y 68 del archivo *prog.py*, para ello use la información suministrada por el datasheet. La mejor forma de garantizar la programación es percatarse que el código este en capacidad de cargar el firmware en dicha memoria flash, dado el caso que no sea capaz, debe modificar el código conforme a las recomendaciones del fabricante, esto lo puede hacer a partir de la línea 144 del archivo *prog.py*, específicamente en el procedimiento *SetupChipCommands*.
