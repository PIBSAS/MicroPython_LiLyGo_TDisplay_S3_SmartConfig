import s3lcd, tft_config, time
import romanc as vector_font
import vga1_8x8 as font
import chango_16 as bitmap_font

tft =tft_config.config(3)
tft.init()

tft.text(font, "Hello World", 0, 0)
tft.draw(vector_font, "Hello World", 0, 30 )
tft.write(bitmap_font, "Hello World", 0, 60)
tft.show()
# END CODE