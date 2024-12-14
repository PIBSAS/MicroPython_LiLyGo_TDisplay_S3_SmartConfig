import tft_config
import s3lcd
import vga2_bold_16x32 as font
import time
""" Inicializamos la interfaz """
tft = tft_config.config(3)
tft.init()
tft.fill(s3lcd.WHITE)

""" Constantes """
ancho = tft.width() # == 170 pixel
alto = tft.height() # == 320 pixel
print(f"{ancho} x {alto}")
print(f"ancho:{font.WIDTH} alto:{font.HEIGHT}")
#tft.text(font,'Micro',ancho//2,0,s3lcd.RED,s3lcd.WHITE)
#for char in range(font.FIRST, font.LAST):
#    tft.text(font, chr(char), ancho //2, 33, s3lcd.MAGENTA, s3lcd.WHITE)
#    tft.text(font,chr(153), ancho //2, 90, s3lcd.MAGENTA, s3lcd.WHITE)
    
#    time.sleep(1)
#    tft.show()
#tft.hline(0,33,ancho//2,s3lcd.GREEN)

tft.fill(s3lcd.BLUE)
line = 0
col = 0
for char in range(70,180):
    tft.text(font, chr(char), col, line, s3lcd.WHITE, s3lcd.BLUE)
    tft.show()
    col += font.WIDTH
    if col > tft.width() - font.WIDTH:
        col = 0
        line += font.HEIGHT

        if line > tft.height() - font.HEIGHT:
            time.sleep(3)
            tft.fill(s3lcd.BLUE)
            line = 0
            col = 0

time.sleep(3)
tft.show()
