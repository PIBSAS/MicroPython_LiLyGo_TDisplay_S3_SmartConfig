from machine import Pin
from time import sleep
"""LCD_BL PIN is GPIO38"""
bl = Pin(38, Pin.OUT)

try:
    while True:
        bl.value(0)
        sleep(1)
        bl.value(1)
        sleep(1)
except Exception as e:
    print("Enchufa la placa man!", e)
"""END CODE"""