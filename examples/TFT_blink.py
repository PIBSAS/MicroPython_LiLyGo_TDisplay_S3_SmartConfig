import s3lcd
from tft_config import config
from time import sleep

tft = config(0)
tft.init()

try:
    while True:
        # Encender pantalla en blanco
        tft.fill(s3lcd.WHITE)
        tft.show()
        sleep(1)
        # Encender pantalla en negro
        tft.fill(s3lcd.BLACK)
        tft.show()
        sleep(1)
except Exception as e:
    print("Enchufa la placa man!", e)
# END CODE