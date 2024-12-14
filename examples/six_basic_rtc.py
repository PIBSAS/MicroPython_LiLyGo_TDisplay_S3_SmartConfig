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

BUG en los anteriore tome WeekDay como semana y era dia de la semana y es asi:
0: Lunes
1: Martes
2: Miércoles
3: Jueves
4: Viernes
5: Sábado
6: Domingo
"""
from machine import RTC

fechin = RTC()
fechin.datetime((2024,10,5,1,0,0,0,0))
pasado = [None] * 8
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

while True:
    f = fechin.datetime() # Preguntamos la fecha completa y la guardamos en f
    """ Creamos solo un Flag booleano para detectar cambios, inicializado en False "Sin Cambios" """
    cambios = False
    for cambio in range(8):
        if f[cambio] != pasado[cambio]:
            cambios = True # Porque hubo cambios
            pasado[cambio] = f[cambio]
    
    if cambios:
        print(f"\rAño: {f[0]}, Mes: {f[1]}, Día: {f[2]}, Hoy es: {dias[f[3]]}, Hora: {f[4]}, Minuto: {f[5]}, Segundos: {f[6]}", end="")