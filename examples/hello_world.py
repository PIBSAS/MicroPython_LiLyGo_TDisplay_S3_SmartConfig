import s3lcd, tft_config, time
import romanc as vector_font
import vga1_8x8 as font
import chango_16 as bitmap_font

tft = tft_config.config(3)
tft.init()

frase = "Hello World"
tft.text(font, frase, 0, 0)
tft.draw(vector_font, frase, 0, 30)
tft.write(bitmap_font, frase, 0, 60)
tft.show()
# END CODE