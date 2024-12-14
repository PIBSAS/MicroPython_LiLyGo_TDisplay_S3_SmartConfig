import tft_config
import s3lcd
import inconsolata_16 as f
import time
""" Vector Fonts son:
 - Astrol
 - Cyrilc
 - Gotheng
 - Gother
 - Gothita
 - Greekc
 - Greekcs
 - Greekp
 - Greeks
 - Italicc
 - Italiccs
 - Italict
 - Lowmat
 - Marker
 - Meteo
 - Music
 - Romanc
 - Romancs
 - Romand
 - Romanp
 - Romans
 - Romant
 - Scriptc
 - Scripts
 - Symbol
 - Uppmat
 """
""" Bitmap Fonts son:
 - VGA todas
"""
""" Inicializamos la interfaz """
tft = tft_config.config()
tft.init()
tft.fill(s3lcd.WHITE)

""" Constantes """
ancho = tft.width() # == 170 pixel
alto = tft.height() # == 320 pixel
#print(f"{ancho} x {alto}")
""" escribimos fuentes usando text(fuente, texto, donde inicia x, inicio y, color)"""
#fuente = [vga1_bold_16x16,vga1_bold_16x32,vga2_16x16,vga2_8x16,vga2_8x8,vga2_bold_16x16,vga2_bold_16x32]
"""
    text():
    - NotoSansMono_32 falla KeyError: WIDTH
    - NotoSans_32 idem
    - NotoSerif_32 idem
    - greekc,greekcs,greekp,greeks falla ilegible
    - inconsolata_16 y 32 FIRST
    - italicc,italiccs,italict ilegible
    - marker ilegible
    - meteo ilegible
    - music ilegible
    - romanc,romancs,romand,romanp,romans,romant ilegible
    - scriptc,scripts ilegible
    - symbol ilegible
    - vga1_8x8,vga1_8x16,vga1_16x16,vga1_16x32 ok
    - vga1_bold_16x16,vga1_bold_16x32,vga2_16x16,vga2_8x16,vga2_8x8,vga2_bold_16x16,vga2_bold_16x32 ok
    
    draw():
    - NotoSansMono_32 falla KeyError: INDEX
    - NotoSans_32 ==
    - NotoSerif_32 ==
    - greekc, greekcs,greekp,greeks ok
    - inconsolata_16 INDEX
    - italicc,italiccs,italict ok
    - marker ok
    - meteo ok
    - music ok
    - romanc,romancs,romand,romanp,romans,romant ok
    - scriptc,scripts ok
    - symbol ok
    - vga1_8x8,vga1_8x16,vga1_16x16,vga1_16x32 INDEX
    - vga1_bold_16x16,vga1_bold_16x32,vga2_16x16,vga2_8x16,vga2_8x8,vga2_bold_16x16,vga2_bold_16x32 INDEX
    
    write():
    - NotoSansMono_32
    - NotoSans_32
    - NotoSerif_32
    - greekc, greekcs,greekp,greeks falla BPP
    - inconsolata_16 OFFSET_WIDTH
    - italicc,italiccs,italict BPP
    - marker BPP
    - meteo BPP
    - music BPP
    - romanc,romancs,romand,romanp,romans,romant BPP
    - scriptc,scripts BPP
    - symbol BPP
    - vga1_8x8,vga1_8x16,vga1_16x16,vga1_16x32 BPP
    - vga1_bold_16x16,vga1_bold_16x32,vga2_16x16,vga2_8x16,vga2_8x8,vga2_bold_16x16,vga2_bold_16x32 BPP

"""
texto = "Aerola"
tft.write(f,texto,ancho//2,alto//2,s3lcd.BLUE)
tft.show()
time.sleep(1)
tft.deinit()