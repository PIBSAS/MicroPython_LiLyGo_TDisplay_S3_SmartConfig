import s3lcd, tft_config, time, ntptime
import NotoSerif_32 as font
import network
from machine import RTC
import math

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
ntptime.host = "time.nist.gov"  # Se puede cambiar de donde obtenemos la hora
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

def fillSmoothRoundRect(x, y, w, h, r, color):
    # Asegúrate de que el tamaño del rectángulo no exceda los límites de la pantalla
    if x < 0 or y < 0 or x + w > 320 or y + h > 170:
        print("El rectángulo está fuera de los límites de la pantalla.")
        return

    # Llenar el área central del rectángulo (sin las esquinas)
    tft.fill_rect(x + r, y, w - 2 * r, h, color)  # Parte central
    tft.fill_rect(x, y + r, w, h - 2 * r, color)  # Parte vertical

    # Dibujar las esquinas redondeadas
    for angle in range(0, 90):  # Dibujar arcos en 90 grados
        rad = math.radians(angle)

        # Calcular las posiciones de las esquinas
        corner_x1 = x + r - int(r * math.cos(rad))
        corner_y1 = y + r - int(r * math.sin(rad))
        corner_x2 = x + w - r + int(r * math.cos(rad))
        corner_y2 = y + r - int(r * math.sin(rad))
        corner_x3 = x + r - int(r * math.cos(rad))
        corner_y3 = y + h - r + int(r * math.sin(rad))
        corner_x4 = x + w - r + int(r * math.cos(rad))
        corner_y4 = y + h - r + int(r * math.sin(rad))

        # Rellenar píxeles en el arco
        for i in range(r):  # Solo dibuja hasta el radio
            # Esquina superior izquierda
            tft.pixel(corner_x1, corner_y1 + i, color)
            # Esquina superior derecha
            tft.pixel(corner_x2, corner_y2 + i, color)
            # Esquina inferior izquierda
            tft.pixel(corner_x3, corner_y3 - i, color)
            # Esquina inferior derecha
            tft.pixel(corner_x4, corner_y4 - i, color)

# Dimensiones del rectángulo
ancho_rect = 68
alto_rect = 100
radio = 10
separacion = 20  # Aumentar separación entre rectángulos

# Calcular el ancho total y la altura total
ancho_total = 3 * ancho_rect + 2 * separacion
alto_total = alto_rect  # Solo un rectángulo en altura

# Calcular la posición inicial para centrar horizontal y verticalmente
pos_x = (320 - ancho_total) // 2  # Centrar horizontalmente
pos_y = (170 - alto_total) // 2  # Centrar verticalmente

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

            # Dibujar los rectángulos redondeados para la hora
            fillSmoothRoundRect(pos_x, pos_y, ancho_rect, alto_rect, radio, s3lcd.RED)  # Hora
            fillSmoothRoundRect(pos_x + ancho_rect + separacion, pos_y, ancho_rect, alto_rect, radio, s3lcd.RED)  # Minutos
            fillSmoothRoundRect(pos_x + 2 * (ancho_rect + separacion), pos_y, ancho_rect, alto_rect, radio, s3lcd.RED)  # Segundos

            # Escribir la hora, minutos y segundos en el centro de los rectángulos
            tft.write(font, f"{f[4]:02d}", pos_x + (ancho_rect // 2) - 16, pos_y + (alto_rect // 2) - 16, s3lcd.WHITE, s3lcd.RED)  # Hora (centrado vertical y horizontal)
            tft.write(font, f"{f[5]:02d}", pos_x + ancho_rect + separacion + (ancho_rect // 2) - 16, pos_y + (alto_rect // 2) - 16, s3lcd.WHITE, s3lcd.RED)  # Minutos (centrado vertical y horizontal)
            tft.write(font, f"{f[6]:02d}", pos_x + 2 * (ancho_rect + separacion) + (ancho_rect // 2) - 16, pos_y + (alto_rect // 2) - 16, s3lcd.WHITE, s3lcd.RED)  # Segundos (centrado vertical y horizontal)

            # Calcular la posición para los puntos entre los rectángulos
            punto_y1 = pos_y + (alto_rect // 2) + (separacion // 4) - (separacion + (separacion // 2)) # Centro entre horas y minutos
            punto_y2 = pos_y + alto_rect // 2 + (alto_rect // 4)  # Centrar verticalmente con respecto a los rectángulos
            # Primera posición del punto a la derecha del rectángulo de horas
            punto_x1 = pos_x + ancho_rect + separacion // 2
            punto_x2 = pos_x + ancho_rect + ancho_rect + separacion + separacion // 2

            # Dibujar los puntos entre hora y mminutos
            tft.fill_circle(punto_x1,punto_y1, 6,s3lcd.BLACK)
            tft.fill_circle(punto_x1,punto_y2, 6,s3lcd.BLACK)
            tft.fill_circle(punto_x2,punto_y1, 6,s3lcd.BLACK)
            tft.fill_circle(punto_x2,punto_y2, 6,s3lcd.BLACK)
            tft.show()
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    tft.deinit()
# END CODE
