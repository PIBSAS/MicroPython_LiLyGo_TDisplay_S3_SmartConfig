import s3lcd, tft_config
import math

# Inicializar la pantalla
tft = tft_config.config(3)
tft.init()

def fillSmoothRoundRect(x, y, w, h, r, color):
    # Asegúrate de que el tamaño del rectángulo no exceda los límites de la pantalla
    if x < 0 or y < 0 or x + w > 320 or y + h > 170:
        print("El rectángulo está fuera de los límites de la pantalla.")
        return

    # Llenar el área central del rectángulo
    tft.fill_rect(x + r, y, w - 2 * r, h, color)  # Parte central
    tft.fill_rect(x, y + r, w, h - 2 * r, color)  # Parte vertical

    # Dibujar las esquinas redondeadas
    for angle in range(0, 90):  # Dibujar arcos en 90 grados
        rad = math.radians(angle)

        # Calcular las posiciones de las esquinas
        corner_x1 = x + r - int(r * math.cos(rad))
        corner_y1 = y + r - int(r * math.sin(rad))
        corner_x2 = x + w - r + int(r * math.cos(rad))
        corner_y2 = y + r - int(r * math.sin(rad))
        corner_x3 = x + r - int(r * math.cos(rad))
        corner_y3 = y + h - r + int(r * math.sin(rad))
        corner_x4 = x + w - r + int(r * math.cos(rad))
        corner_y4 = y + h - r + int(r * math.sin(rad))

        # Rellenar píxeles en el arco
        for i in range(1, r):
            # Esquina superior izquierda
            tft.pixel(corner_x1, corner_y1 + i, color)
            # Esquina superior derecha
            tft.pixel(corner_x2, corner_y2 + i, color)
            # Esquina inferior izquierda
            tft.pixel(corner_x3, corner_y3 - i, color)
            # Esquina inferior derecha
            tft.pixel(corner_x4, corner_y4 - i, color)

    # Rellenar los píxeles en el centro del arco para asegurarnos de que estén sólidos
    for angle in range(0, 360):
        rad = math.radians(angle)
        tft.pixel(x + r + int(r * math.cos(rad)), y + r - int(r * math.sin(rad)), color)
        tft.pixel(x + w - r + int(r * math.cos(rad)), y + r - int(r * math.sin(rad)), color)
        tft.pixel(x + r + int(r * math.cos(rad)), y + h - r + int(r * math.sin(rad)), color)
        tft.pixel(x + w - r + int(r * math.cos(rad)), y + h - r + int(r * math.sin(rad)), color)

# Ejemplo de uso de fillSmoothRoundRect
fillSmoothRoundRect(0, 37, 68, 100, 10, s3lcd.RED)  # Color rojo

# Actualizar la pantalla
tft.show()

# Deshabilitar la pantalla al final (si es necesario)
# tft.deinit()
