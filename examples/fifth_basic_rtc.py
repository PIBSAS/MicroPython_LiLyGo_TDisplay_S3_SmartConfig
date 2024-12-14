"""
RTC
classmachine.RTC(id=0, ...)
LA USAMOS ASI:
from machine import RTC
DECLARAMOS UN OBJETO rtc AL CUAL LE ASIGNAMOS LA INICIALIZACION DEL OBJETO RTC()
rtc = RTC()

CONFIGURAMOS UNA FECHA INICIAL LUEGO SOLO LA OBTENDREMOS.
RECIBE UN TUPLE DE TAMAÑO 8:
(YEAR, MONTH, DAY, WEEKDAY, HOURS, MINUTES,SECONDS, SUBSECONDS)
ES DECIR LE ESTOY PASANDO:
YEAR: 2017
MONTH: 8
DAY: 23
WEEKDAY: 1
HOURS: 12
MINUTES: 48
SECONDS: 0
SUBSECONDS 0
rtc.datetime((2017, 8, 23, 1, 12, 48, 0, 0)) # set a specific date and time
YA CONFIGURADA LA LLAMAMOS PARA VER LA FECHA
rtc.datetime() # get date and time

PARA VER QUE OTROS METODOS TIENE ESCRIBIMOS:
dir(rtc) en el REPL de MicroPython
>>> dir(rtc)
['__class__', 'datetime', 'init', 'memory']

"""
from machine import RTC
fechin = RTC()
fechin.datetime((2024,10,5,1,0,0,0,0))
"""Ya Obsoleto
año_pasado = None
mes_anterior = None
ayer = None
la_semana_mmm = None
se_nos_paso = None
primicia = None
fugaz = None
ñoño = None
"""
"""Mas simple:
año_pasado = mes_anterior = ayer = la_semana_mmm = se_nos_paso = primicia = fugaz = ñoño = None
"""
""" Aun más simple:
    Declaramos una variable pasado de tiempo pasado, le asignamos una lista de tamaño 8, la cantidad de variables que habiamos declarado antes.
"""
pasado = [None] * 8

while True:
    f = fechin.datetime() # Preguntamos la fecha completa y la guardamos en f
    """Reducimos esto
    if f[0] != año_pasado:
        print(f"año: {f[0]}") # Acccedemos al año nada más
        año_pasado = f[0]
    if f[1] != mes_anterior:
        print(f"mes: {f[1]}") # Acccedemos al mes nada más
        mes_anterior = f[1]
    if f[2] != ayer:
        print(f"día: {f[2]}") # Acccedemos al día nada más
        ayer = f[2]
    if f[3] != la_semana_mmm:
        print(f"semana: {f[3]}") # Acccedemos a la semana nada más
        la_semana_mmm = f[3]
    if f[4] != se_nos_paso:
        print(f"hora: {f[4]}") # Acccedemos a la hora nada más
        se_nos_paso = f[4]
    if f[5] != primicia:
        print(f"minuto: {f[5]}") # Acccedemos a los minutos nada más
        primicia = f[5]
    if f[6] != fugaz:
        print(f"segundos: {f[6]}") # Acccedemos a los segundos nada más
        fugaz = f[6]
    
    if f[7] != ñoño:
        print(f"sub segundos: {f[7]}") # ÑOÑO! pa que???
        ñoño = f[7]
    """
    """ Si estamos fijandonos continuamente, que año es?,  ya paso el día?, en que semana estamos?, etc, etc
        Y luego vamos a hacer un print del cambio, y asignar el muevo valor a la variable, entonces, porque no hacemos un if con esa condicion!
        De paso, mostramos siempre los valores que queremos, y obviamente a partir de aca ya podemos alternarlos a nuestro antojo.
        Pero en este caso, la reasignación de variables se hará finalizado el bucle y no dentro de este.
        Se podría mejorar solo almacenando la variable que cambia, pero paso a paso.
    """
    
    """ Creamos una lista que almacene los cambios"""
    cambios = []
    for cambio in range(0, 8):
        if f[cambio] != pasado[cambio]:
            cambios.append(cambio)
            pasado[cambio] = f[cambio]
    
    """ Si hubo cambios mostramos el print"""
    """ Ya sin este bodoque  
    if f[0] != año_pasado or f[1] != mes_anterior or f[2] != ayer or f[3] != la_semana_mmm or f[4] != se_nos_paso or f[5] != primicia or f[6] != fugaz:
    """
    if cambios:
        print(f"Año: {f[0]}, Mes: {f[1]}, Día: {f[2]}, Semana: {f[3]}, Hora: {f[4]}, Minuto: {f[5]}, Segundos: {f[6]}")
    
    """ desempaquetamos la tupla para saber si hay cambios y almacenamos solo el cambio, y el resto se deja intacto.
        tupla(valor si es True, condicion es igual o no?, valor si es False.)
        Que significa valor si es True, que hubo cambio y almacenamos el nuevo valor.
        Que significa valor si es False, que no hubo cambio y no hacemos nada
    """
    """ Esto lo reemplazamos gracias al bucle for.
    año_pasado, mes_anterior, ayer, la_semana_mmm, se_nos_paso, primicia, fugaz = (
            f[0] if f[0] != año_pasado else año_pasado,
            f[1] if f[1] != mes_anterior else mes_anterior,
            f[2] if f[2] != ayer else ayer,
            f[3] if f[3] != la_semana_mmm else la_semana_mmm,
            f[4] if f[4] != se_nos_paso else se_nos_paso,
            f[5] if f[5] != primicia else primicia,
            f[6] if f[6] != fugaz else fugaz
        )
    """
"""
Creamos un bucle infinito para que se pregunte si hay cambios en alguna parte de la tupla.
Mediante el uso de condicional if, esto obviamente solo mostrará cambios en f[7] continuamente, y en f[6] cada un segunndo, y en f[5] cada 60 segundos. 
"""