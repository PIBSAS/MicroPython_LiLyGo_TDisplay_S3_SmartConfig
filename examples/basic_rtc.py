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
f = fechin.datetime() # Preguntamos la fecha completa y la guardamos en f
print(f"año: {f[0]}") # Acccedemos al año nada más
print(f"mes: {f[1]}") # Acccedemos al mes nada más
print(f"día: {f[2]}") # Acccedemos al día nada más
print(f"semana: {f[3]}") # Acccedemos a la semana nada más
print(f"hora: {f[4]}") # Acccedemos a la hora nada más
print(f"minuto: {f[5]}") # Acccedemos a los minutos nada más
print(f"segundos: {f[6]}") # Acccedemos a los segundos nada más
print(f"sub segundos: {f[7]}") # ÑOÑO! pa que???

"""
OBVIAMENTE AL EJECUTARSE ASI NO TIENE SENTIDO ALGUNO, ESTAS PONIENDO LA HORA EN UN PUNTO ESPECIFICO
Y  LLAMAS UNA VEZ POR EJECUCION, TENES QUE METER EN UN BUCLE, PARA QUE PREGUNTAR LA FECHA TENGA SENTIDO Y GRACIA
PERO TAMOS VIENDO CHE NO JODAS
"""