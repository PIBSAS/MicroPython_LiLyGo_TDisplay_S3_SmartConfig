import s3lcd
from tft_config import config
import math

color= s3lcd.color565(17,35,222) #RGB
tft = config(3)
tft.init()
tft.fill(color)
tft.pixel(tft.width()//2, tft.height()//2,s3lcd.color565(23,7,27))
for i in range(10):
    tft.circle(tft.width()//2, tft.height()//2,i*9,s3lcd.color565(14,59,2))
tft.show()
