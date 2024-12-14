import math


import s3lcd
from tft_config import config

display = config()
display.init()

x = 85
y = 100
r1 = 75
r2 = 60
a1 = 0 # Graados el cero esta en la parte inferior
a2 = 270
arc_color = s3lcd.MAGENTA
bg_color = s3lcd.BLACK

def draw_smooth_arc(display, x, y, r, ir, start_angle, end_angle, fg_color, bg_color, round_ends=True):
    # start_angle y end_angle en grados, r es radio externo, ir es radio interno
    # Colores fg_color (foreground) y bg_color (background)
    
    if end_angle != start_angle and (start_angle != 0 or end_angle != 360):
        sx = -math.sin(math.radians(start_angle))
        sy = math.cos(math.radians(start_angle))
        ex = -math.sin(math.radians(end_angle))
        ey = math.cos(math.radians(end_angle))

        if round_ends:
            # Extremos redondeados
            sx = sx * (r + ir) / 2.0 + x
            sy = sy * (r + ir) / 2.0 + y
            draw_spot(display, sx, sy, (r - ir) / 2.0, fg_color, bg_color)

            ex = ex * (r + ir) / 2.0 + x
            ey = ey * (r + ir) / 2.0 + y
            draw_spot(display, ex, ey, (r - ir) / 2.0, fg_color, bg_color)
        else:
            # Extremos cuadrados
            asx = sx * ir + x
            asy = sy * ir + y
            aex = sx * r + x
            aey = sy * r + y
            draw_wedge_line(display, asx, asy, aex, aey, 0.3, 0.3, fg_color, bg_color)

            asx = ex * ir + x
            asy = ey * ir + y
            aex = ex * r + x
            aey = ey * r + y
            draw_wedge_line(display, asx, asy, aex, aey, 0.3, 0.3, fg_color, bg_color)

        # Dibuja el arco
        draw_arc(display, x, y, r, ir, start_angle, end_angle, fg_color, bg_color)
    else:
        # Dibuja un arco completo de 360 grados
        draw_arc(display, x, y, r, ir, 0, 360, fg_color, bg_color)

# Funciones auxiliares que debes implementar en tu código:

def draw_spot(display, x, y, radius, fg_color, bg_color):
    # El círculo lleno se puede crear usando la función draw_wedge_line con longitud de línea cero
    draw_wedge_line(display, ax, ay, ax, ay, r, r, fg_color, bg_color)

def draw_wide_line(display, ax, ay, bx, by, wd, fg_color, bg_color):
    # Dibuja una línea con extremos redondeados usando draw_wedge_line
    draw_wedge_line(display, ax, ay, bx, by, wd / 2.0, wd / 2.0, fg_color, bg_color)
    
def draw_wedge_line(display, ax, ay, bx, by, ar, br, fg_color, bg_color):
    if ar < 0.0 or br < 0.0:
        return
    if abs(ax - bx) < 0.01 and abs(ay - by) < 0.01:
        bx += 0.01  # Evita división por cero

    # Encuentra el bounding box de la línea
    x0 = int(math.floor(min(ax - ar, bx - br)))
    x1 = int(math.ceil(max(ax + ar, bx + br)))
    y0 = int(math.floor(min(ay - ar, by - br)))
    y1 = int(math.ceil(max(ay + ar, by + br)))

    # Verifica si la ventana está dentro de los límites
    if not clip_window(display, x0, y0, x1, y1):
        return

    # Establece los puntos iniciales x e y
    ys = ay
    if (ax - ar) > (bx - br):
        ys = by

    rdt = ar - br  # Delta del radio
    alpha = 1.0
    ar += 0.5

    bg = bg_color
    bax = bx - ax
    bay = by - ay

    begin_write(display)  # Inicia la escritura en el display
    in_transaction = True

    xs = x0
    # Recorre el bounding box desde ys hacia abajo, calculando la intensidad de píxeles
    for yp in range(ys, y1 + 1):
        swin = True  # Indicador para comenzar una nueva ventana
        end_x = False  # Indicador para saltar píxeles
        ypay = yp - ay
        for xp in range(xs, x1 + 1):
            if end_x and alpha <= LoAlphaThreshold:
                break  # Salta el lado derecho
            xpax = xp - ax
            alpha = ar - wedge_line_distance(xpax, ypay, bax, bay, rdt)
            if alpha <= LoAlphaThreshold:
                continue
            if not end_x:
                end_x = True
                xs = xp
            if alpha > HiAlphaThreshold:
                draw_pixel(display, xp, yp, fg_color)
                continue
            # Mezcla el color con el fondo y dibuja
            if bg_color == 0x00FFFFFF:
                bg = read_pixel(display, xp, yp)
            blended_color = fast_blend(int(alpha * PixelAlphaGain), fg_color, bg)
            draw_pixel(display, xp, yp, blended_color)

    # Restablece el inicio de x al lado izquierdo del bounding box
    xs = x0
    # Recorre el bounding box desde ys hacia arriba
    for yp in range(ys - 1, y0 - 1, -1):
        swin = True  # Indicador para comenzar una nueva ventana
        end_x = False  # Indicador para saltar píxeles
        ypay = yp - ay
        for xp in range(xs, x1 + 1):
            if end_x and alpha <= LoAlphaThreshold:
                break  # Salta el lado derecho de la línea dibujada
            xpax = xp - ax
            alpha = ar - wedge_line_distance(xpax, ypay, bax, bay, rdt)
            if alpha <= LoAlphaThreshold:
                continue
            if not end_x:
                end_x = True
                xs = xp
            if alpha > HiAlphaThreshold:
                draw_pixel(display, xp, yp, fg_color)
                continue
            # Mezcla el color con el fondo y dibuja
            if bg_color == 0x00FFFFFF:
                bg = read_pixel(display, xp, yp)
            blended_color = fast_blend(int(alpha * PixelAlphaGain), fg_color, bg)
            draw_pixel(display, xp, yp, blended_color)

    in_transaction = False
    end_write(display)  # Finaliza la escritura en el display

# Funciones auxiliares que debes implementar en tu código:

def clip_window(xs, ys, xe, ye, _xDatum, _yDatum, _vpX, _vpY, _vpW, _vpH, _vpOoB):
    if _vpOoB:
        return False  # El área está fuera del viewport

    # Ajustar las coordenadas con los valores de desplazamiento (_xDatum y _yDatum)
    xs[0] += _xDatum
    ys[0] += _yDatum
    xe[0] += _xDatum
    ye[0] += _yDatum

    # Verifica si el área está fuera del viewport
    if xs[0] >= _vpW or ys[0] >= _vpH:
        return False  # El área está fuera del viewport
    if xe[0] < _vpX or ye[0] < _vpY:
        return False  # El área está fuera del viewport

    # Recortar los límites del área de dibujo
    if xs[0] < _vpX:
        xs[0] = _vpX
    if ys[0] < _vpY:
        ys[0] = _vpY
    if xe[0] > _vpW:
        xe[0] = _vpW - 1
    if ye[0] > _vpH:
        ye[0] = _vpH - 1

    return True  # El área está total o parcialmente dentro del viewport

def wedge_line_distance(xpax, ypay, bax, bay, dr):
    h = max(min((xpax * bax + ypay * bay) / (bax * bax + bay * bay), 1.0), 0.0)
    dx = xpax - bax * h
    dy = ypay - bay * h
    return (dx * dx + dy * dy) ** 0.5 + h * dr


def fast_blend(alpha, fgc, bgc):
    # Separar y mezclar los canales de rojo y azul de 5 bits
    rxb = bgc & 0xF81F
    rxb += ((fgc & 0xF81F) - rxb) * (alpha >> 2) >> 6
    
    # Separar y mezclar el canal verde de 6 bits
    xgx = bgc & 0x07E0
    xgx += ((fgc & 0x07E0) - xgx) * alpha >> 8
    
    # Recombinar los canales
    return (rxb & 0xF81F) | (xgx & 0x07E0)

def drawPixel(self, x, y, color):
    # Ajuste del origen de los datos si es necesario
    x += self._xDatum
    y += self._yDatum

    # Verificación de límites
    if (x < self._vpX or y < self._vpY or x >= self._vpW or y >= self._vpH):
        return

    # Comienza la escritura al TFT
    self.begin_tft_write()

    # Establece la dirección de la ventana donde se dibujará el pixel
    self.write_command(TFT_CASET)
    self.write_data16(x)  # Columna
    self.write_data16(x)

    self.write_command(TFT_PASET)
    self.write_data16(y)  # Fila
    self.write_data16(y)

    # Escribe el color del pixel en la memoria RAM del TFT
    self.write_command(TFT_RAMWR)
    self.write_data16(color)

    # Termina la escritura al TFT
    self.end_tft_write()

def begin_tft_write(self):
    if self.locked:
        self.locked = False  # Marca que el acceso SPI ahora está desbloqueado

        # No hay equivalente directo en MicroPython para beginTransaction, 
        # pero podrías manejar configuraciones específicas aquí si es necesario.

        self.cs.value(0)  # Selecciona CS (baja el pin CS)
        self.set_bus_write_mode()  # Cambia el modo del bus a escritura

def begin_nin_write(self):
    # Igual que begin_tft_write pero no inlineado
    self.begin_tft_write()

def end_tft_write(self):
    if not self.inTransaction:  # Verifica si no estamos en una transacción
        if not self.locked:     # Verifica si SPI está bloqueada
            self.locked = True  # Marca que el acceso SPI está bloqueado
            self.spi_busy_check()  # Verifica que la transmisión SPI haya terminado
            self.cs.value(1)    # Deselect CS (levanta el pin CS)
            self.set_bus_read_mode()  # Cambia el modo del bus a lectura si es necesario

def end_nin_write(self):
    # Igual que end_tft_write pero no inlineado, por lo que puede ser modificado si es necesario
    self.end_tft_write()

def read_pixel(self, x0, y0):
    if self._vpOoB:
        return 0

    x0 += self._xDatum
    y0 += self._yDatum

    # Verificación de rango
    if (x0 < self._vpX) or (y0 < self._vpY) or (x0 >= self._vpW) or (y0 >= self._vpH):
        return 0

    if not self.inTransaction:
        self.cs.value(0)  # CS_L

    self.read_addr_window(x0, y0, 1, 1)

    # Configura pines D0-D7 como entrada
    self.bus_dir(GPIO_DIR_MASK, INPUT)

    # Leer el byte dummy para descartar valor irrelevante
    self.read_byte()

    # Leer el pixel BRG de 16 bits
    rgb = ((self.read_byte() & 0xF8) << 8) | ((self.read_byte() & 0xFC) << 3) | (self.read_byte() >> 3)

    if not self.inTransaction:
        self.cs.value(1)  # CS_H

    # Configura pines D0-D7 como salida
    self.bus_dir(GPIO_DIR_MASK, OUTPUT)

    return rgb

def drawArc(self, x, y, r, ir, startAngle, endAngle, fg_color, bg_color, smooth=True):
    if endAngle > 360: endAngle = 360
    if startAngle > 360: startAngle = 360
    if self._vpOoB or startAngle == endAngle: return
    if r < ir: r, ir = ir, r  # Ensure r > ir
    if r <= 0 or ir < 0: return  # Invalid r, ir can be zero (circle sector)

    if endAngle < startAngle:
        # Arc sweeps through 6 o'clock so draw in two parts
        if startAngle < 360: 
            self.drawArc(x, y, r, ir, startAngle, 360, fg_color, bg_color, smooth)
        if endAngle == 0: return
        startAngle = 0

    self.inTransaction = True

    xs = 0  # x start position for quadrant scan
    alpha = 0  # alpha value for blending pixels

    r2 = r * r  # Outer arc radius^2
    if smooth: r += 1  # Outer AA zone radius
    r1 = r * r  # Outer AA radius^2
    w = r - ir  # Width of arc (r - ir + 1)
    r3 = ir * ir  # Inner arc radius^2
    if smooth: ir -= 1  # Inner AA zone radius
    r4 = ir * ir  # Inner AA radius^2

    # Fill in start slope table
    startSlope = [0, 0, 0xFFFFFFFF, 0]
    endSlope = [0, 0xFFFFFFFF, 0, 0]

    # Ensure maximum U16.16 slope of arc ends is ~ 0x8000 0000
    minDivisor = 1.0 / 0x8000

    # Calculate slopes for start angle
    fabscos = abs(math.cos(math.radians(startAngle)))
    fabssin = abs(math.sin(math.radians(startAngle)))
    slope = int((fabscos / (fabssin + minDivisor)) * (1 << 16))

    # Update slope table for start angle
    if startAngle <= 90:
        startSlope[0] = slope
    elif startAngle <= 180:
        startSlope[1] = slope
    elif startAngle <= 270:
        startSlope[1] = 0xFFFFFFFF
        startSlope[2] = slope
    else:
        startSlope[1] = 0xFFFFFFFF
        startSlope[2] = 0
        startSlope[3] = slope

    # Calculate slopes for end angle
    fabscos = abs(math.cos(math.radians(endAngle)))
    fabssin = abs(math.sin(math.radians(endAngle)))
    slope = int((fabscos / (fabssin + minDivisor)) * (1 << 16))

    if endAngle <= 90:
        endSlope[0] = slope
        endSlope[1] = 0
        startSlope[2] = 0
    elif endAngle <= 180:
        endSlope[1] = slope
        startSlope[2] = 0
    elif endAngle <= 270:
        endSlope[2] = slope
    else:
        endSlope[3] = slope

    # Scan quadrant
    for cy in range(r - 1, 0, -1):
        length = [0, 0, 0, 0]  # Pixel run length
        xst = [-1, -1, -1, -1]  # Pixel run x start
        dy2 = (r - cy) * (r - cy)

        # Find and track arc zone start point
        while (r - xs) * (r - xs) + dy2 >= r1:
            xs += 1

        for cx in range(xs, r):
            # Calculate radius^2
            hyp = (r - cx) * (r - cx) + dy2

            # If in outer zone calculate alpha
            if hyp > r2:
                alpha = ~self.sqrt_fraction(hyp)  # Outer AA zone
            # If within arc fill zone, get line start and lengths for each quadrant
            elif hyp >= r3:
                # Calculate U16.16 slope
                slope = ((r - cy) << 16) // (r - cx)
                if startSlope[0] >= slope >= endSlope[0]:  # slope hi -> lo
                    xst[0] = cx  # Bottom left line end
                    length[0] += 1
                if startSlope[1] <= slope <= endSlope[1]:  # slope lo -> hi
                    xst[1] = cx  # Top left line end
                    length[1] += 1
                if startSlope[2] >= slope >= endSlope[2]:  # slope hi -> lo
                    xst[2] = cx  # Bottom right line start
                    length[2] += 1
                if endSlope[3] >= slope >= startSlope[3]:  # slope lo -> hi
                    xst[3] = cx  # Top right line start
                    length[3] += 1
                continue  # Next x
            else:
                if hyp <= r4: break  # Skip inner pixels
                alpha = self.sqrt_fraction(hyp)  # Inner AA zone

            if alpha < 16: continue  # Skip low alpha pixels

            # Blend foreground and background color
            pcol = self.fastBlend(alpha, fg_color, bg_color)
            # Check if an AA pixel needs to be drawn
            slope = ((r - cy) << 16) // (r - cx)
            if startSlope[0] >= slope >= endSlope[0]:  # BL
                self.drawPixel(x + cx - r, y - cy + r, pcol)
            if startSlope[1] <= slope <= endSlope[1]:  # TL
                self.drawPixel(x + cx - r, y + cy - r, pcol)
            if startSlope[2] >= slope >= endSlope[2]:  # TR
                self.drawPixel(x - cx + r, y + cy - r, pcol)
            if endSlope[3] >= slope >= startSlope[3]:  # BR
                self.drawPixel(x - cx + r, y - cy + r, pcol)

        # Add line in inner zone
        if length[0]:
            self.drawFastHLine(x + xst[0] - length[0] + 1 - r, y - cy + r, length[0], fg_color)  # BL
        if length[1]:
            self.drawFastHLine(x + xst[1] - length[1] + 1 - r, y + cy - r, length[1], fg_color)  # TL
        if length[2]:
            self.drawFastHLine(x - xst[2] + r, y + cy - r, length[2], fg_color)  # TR
        if length[3]:
            self.drawFastHLine(x - xst[3] + r, y - cy + r, length[3], fg_color)  # BR

    # Fill in center lines
    if startAngle == 0 or endAngle == 360:
        self.drawFastVLine(x, y + r - w, w, fg_color)  # Bottom
    if startAngle <= 90 and endAngle >= 90:
        self.drawFastHLine(x - r + 1, y, w, fg_color)  # Left
    if startAngle <= 180 and endAngle >= 180:
        self.drawFastVLine(x, y - r + 1, w, fg_color)  # Top
    if startAngle <= 270 and endAngle >= 270:
        self.drawFastHLine(x + r - w, y, w, fg_color)  # Right

    self.inTransaction = False
    self.end_tft_write()

def drawFastHLine(self, x, y, w, color):
    if self._vpOoB:
        return

    x += self._xDatum
    y += self._yDatum

    # Clipping
    if y < self._vpY or x >= self._vpW or y >= self._vpH:
        return

    if x < self._vpX:
        w += x - self._vpX
        x = self._vpX

    if x + w > self._vpW:
        w = self._vpW - x

    if w < 1:
        return

    self.begin_tft_write()
    self.setWindow(x, y, x + w - 1, y)
    self.pushBlock(color, w)
    self.end_tft_write()

def drawFastVLine(x, y, h, color, xDatum=0, yDatum=0, vpX=0, vpY=0, vpW=0, vpH=0, vpOoB=False):
    if vpOoB:
        return

    x += xDatum
    y += yDatum

    # Clipping
    if x < vpX or x >= vpW or y >= vpH:
        return

    if y < vpY:
        h += y - vpY
        y = vpY

    if y + h > vpH:
        h = vpH - y

    if h < 1:
        return

    begin_tft_write()
    setWindow(x, y, x, y + h - 1)
    pushBlock(color, h)
    end_tft_write()

def sqrt_fraction(num):
    # Compute the fixed point square root of an integer and
    # return the 8 MS bits of the fractional part.
    # Quicker than sqrt() for processors that do not have an FPU (e.g. RP2040)
    
    if num > 0x40000000:
        return 0

    bsh = 0x00004000
    fpr = 0
    osh = 0

    # Auto adjust from U8:8 up to U15:16
    while num > bsh:
        bsh <<= 2
        osh += 1

    while bsh > 0:
        bod = bsh + fpr
        if num >= bod:
            num -= bod
            fpr = bsh + bod
        num <<= 1
        bsh >>= 1

    return fpr >> osh

display.show()