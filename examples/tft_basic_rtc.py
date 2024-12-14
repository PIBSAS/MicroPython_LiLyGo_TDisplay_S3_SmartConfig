import s3lcd, tft_config, time
import chango_16 as font
from machine import RTC

tft = tft_config.config(3)
tft.init()
fecha = RTC()
fecha.datetime((2024,10,5,5,14,2,0,0))
pasado = [None] * 8
dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

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
            tft.write(font, f"{f[0]}, {f[2]}, {f[1]}", 0, 0)
            tft.write(font, f"Hoy es: {dias[f[3]]}", 0, 20)
            tft.write(font, f"{f[4]:02d}:{f[5]:02d}:{f[6]:02d}", 0, 40)
            tft.show()
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    tft.deinit()
# END CODE