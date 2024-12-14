import tft_config
import s3lcd
import vga1_8x8 as font
import framebuf
""" Inicializamos la interfaz """
tft = tft_config.config()
tft.init()
tft.fill(s3lcd.WHITE)

""" Constantes """
ancho = tft.width() # == 170 pixel
alto = tft.height() # == 320 pixel
print(f"{ancho} x {alto}")

tft.text(font,'Micro',0,0,s3lcd.RED)
tft.hline(0,9,ancho//2,s3lcd.GREEN)
tft.show()