# PROGRAMADOR I2C PARA RTD2660 DESDE RASPBERRY PI
Este repositorio tiene como fin documentar y brindar las herramientas necesarias para programar cualquier tarjeta que use RTD2660 y una memoria flash para guardar el firmware. Se da prioriodad a los drives PCB800099 y PCB800661. Para desarrollar esta guia con exito se requiere haber realizado estos pasos previos:

* Tener pleno acceso a una Raspberry. Si no cuenta con una pantalla, mouse y teclado usb, recomiendo el siguiente tutorial: http://stackoverflow.com/questions/16040128/hook-up-raspberry-pi-via-ethernet-to-laptop-without-router

* Tener activo el I2C de la Raspberry. Para mayor informacion visitar: http://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/

* Contar en la Raspberry con 'python-smbus' y 'i2c-tools'. Los puede instalar desde consola con la siguiente linea:
                  
        sudo apt-get install -y python-smbus i2c-tools

## Como seleccionar el firmware
Si su tarjeta es PCB800099 o PCB800661 puede que el firmware que busca esta en alguna de las carpetas adjuntas, en el caso contrario, la sugerencia es contactar a su proveedor por la firmware conforme a su driver. Desafortunadamente no he encontrado el codigo fuente para generar el firmware.bin, si usted logra obtenerlo y hacerlo funcionar, por favor hagacelo saber al mundo.

Para elegir el firmware tambien hay que tener encuenta la pantalla, espeificamente 3 caracteriticas: resolución, vizualización de color y clase de señal de salida, la forma mas efectiva para obtener esta informacion es por medio del datasheet.

### Ejemplo:
* Pantalla: LTN133AT16 - Datasheet: http://panelone.net/es/13-3-pulgadas/SAMSUNG_LTN133AT16-S01_13.3_pulgadas-datasheet
* Driver: PCB800661

Identificamos:
* Resolución: 1280x800
* Vizualización de color: 262k (6-bits)
* Clase de señal: LVDS

Buscando en la capeta PCB800661 encontramos el firmware 'PCB800661-LVDS1280X800-D6BIT-!HDMI.BIN', en su nombre encontramos la tarjeta PCB800661, la clase de señal LVDS, con resolución 1280X800, y la vizualización de color D6BIT.

## Conexión 
Para realizar la programación del firmware debe realizar la siguiente conexión según la tarjeta:

![Conexión PCB800661](http://img.auctiva.com/imgdata/1/6/7/2/2/0/6/webimg/831951423_o.jpg)

![Conexión PCB800099](http://www.njytouch.com/upload/201410/thumb_dis/1414462539.jpg)

## Ejecución
Antes de la ejecución hay que asegurar la correcta conexión y 
Dentro de la carpeta del repositorio, especificamente donde se encuentra el archivo 'prog.py', ejecutar el
