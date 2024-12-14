import s3lcd, tft_config
import vga1_16x16 as font
##import NotoSans_32 as noto_sans
##import NotoSerif_32 as noto_serif
##import NotoSansMono_32 as noto_mono
# Resolución
# s3lcd.ESPLCD(bus, width, height, {reset, rotations, rotation, inversion, dma_rows, options})
#170x320((170, 320, 35, 0, false, false, false), (320, 170, 0, 35, true, true, false), (170, 320, 35, 0, false, true, true), (320, 170, 0, 35, true, false, true))
tft = tft_config.config(tft_config.WIDE)
tft.init()
tft.fill(s3lcd.BLACK)
tft.show()

def escribo(s,x,y):
    tft.text(font,s, x, y)
    tft.show()

escribo('PEPEPEPEPEREPEPEPEPR',0,0)
escribo('REREREREREPEREREREPE',0,16)
escribo('REREREREREPEREREREPE',0,32)
escribo('REREREREREPEREREREPE',0,48)
escribo('REREREREREPEREREREPE',0,64)
escribo('REREREREREPEREREREPE',0,80)
escribo('REREREREREPEREREREPE',0,96)
escribo('REREREREREPEREREREPE',0,112)
escribo('REREREREREPEREREREPE',0,128)
escribo('REREREREREPEREREREPE',0,144)
tft.deinit()