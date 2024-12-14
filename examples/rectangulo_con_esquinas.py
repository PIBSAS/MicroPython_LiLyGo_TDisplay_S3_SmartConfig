import s3lcd, tft_config

# Inicializar la pantalla
tft = tft_config.config(1)
tft.init()

def fillSmoothRoundRect(x, y, w, h, r, color):
    # Asegúrate de que el tamaño del rectángulo no exceda los límites de la pantalla
    if x < 0 or y < 0 or x + w > 320 or y + h > 170:
        print("El rectángulo está fuera de los límites de la pantalla.")
        return

    # Definir los vértices del polígono para un rectángulo redondeado
    polygon = [
        (x + r, y),  # Esquina superior izquierda
        (x + w - r, y),  # Esquina superior derecha
        (x + w, y + r),  # Esquina superior derecha
        (x + w, y + h - r),  # Esquina inferior derecha
        (x + w - r, y + h),  # Esquina inferior derecha
        (x + r, y + h),  # Esquina inferior izquierda
        (x, y + h - r),  # Esquina inferior izquierda
        (x, y + r)  # Esquina superior izquierda
    ]
    
    # Llenar el rectángulo central
    tft.fill_rect(x + r, y, w - 2 * r, h, color)
    tft.fill_rect(x, y + r, w, h - 2 * r, color)
    
    # Dibujar el polígono
    tft.fill_polygon(polygon, 0, 0, color)

# Ejemplo de uso de fillSmoothRoundRect
fillSmoothRoundRect(21, 37, 68, 100, 10, s3lcd.RED)  # Color rojo

# Actualizar la pantalla
tft.show()

# Dehabilitar la pantalla al final (si es necesario)
#tft.deinit()
