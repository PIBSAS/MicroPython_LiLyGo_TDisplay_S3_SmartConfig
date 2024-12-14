import s3lcd, tft_config, time, ntptime
import NotoSerif_32 as font
import network
from machine import RTC

""" Modo Station """
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('TELWINET:9E-5E_EXT', '68297640')

# Esperar a que se conecte a la red WiFi
while not wlan.isconnected():
    time.sleep(1)
print("Conectado a la red WiFi")

""" Inicializar Pantalla """
tft = tft_config.config(3)
tft.init()

""" Inicializar RTC """
fecha = RTC()
pasado = [None] * 8
dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

""" Función hora """
ntptime.host = "time.nist.gov" # Se puede cambiar de donde obtenemos la hora
def hora():
    try:
        print("Obteniendo la hora desde el servidor NTP...")
        time.sleep(2)
        ntptime.settime()  # Sincroniza el reloj interno con el NTP
        la_hora = time.localtime()  # Obtiene la hora UTC por defecto
        mi_hora = (la_hora[3] - 3) % 24  # Resta 3 horas y ajusta para que esté en el rango 0-23
        # Si ajustamos la hora a UTC-3, debemos revisar el día de la semana
        comprobar_dia = la_hora[2]
        if mi_hora < 0:
            mi_hora += 24
            comprobar_dia -= 1
            if comprobar_dia < 1:  # Ajusta el día si es menor que 1
                comprobar_dia = 31  # Esto se debe ajustar dependiendo del mes y año (simplificado aquí)
                
        fecha.datetime((la_hora[0], la_hora[1], comprobar_dia, la_hora[6] + 1, mi_hora, la_hora[4], la_hora[5], 0))
        print("Ahora si corregido desde NTP")
    except Exception as e:
        print("Error al obtener la hora desde NTP:", e)

hora()

""" Bucle Principal """
try:
    while True:
        f = fecha.datetime()
        cambios = False
        for cambio in range(8):
            if f[cambio] != pasado[cambio]:
                cambios = True
                pasado[cambio] = f[cambio]
        
        if cambios:
            tft.fill(0)
            tft.fill(s3lcd.WHITE)
            #tft.write(font, f"{f[0]}, {f[2]}, {f[1]}", 0, 0)
            #tft.write(font, f"Hoy es: {dias[f[3]]}", 0, 20)
            tft.write(font, f"{f[4]:02d}:{f[5]:02d}:{f[6]:02d}", 100, 65, s3lcd.RED, s3lcd.WHITE)
            tft.show()
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    tft.deinit()
# END CODE
