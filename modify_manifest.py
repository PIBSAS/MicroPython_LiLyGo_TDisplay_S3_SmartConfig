import os

manifest_path = '/home/runner/work/MicroPython_LilyGO_T_Display_S3/MicroPython_LilyGO_T_Display_S3/s3lcd/manifest.py'

# Leer el contenido actual del manifest
with open(manifest_path, 'r') as file:
    content = file.readlines()

# Añadir las líneas necesarias
new_lines = [
    "ADD_FILE('tft_config.py', '/home/runner/work/MicroPython_LilyGO_T_Display_S3/MicroPython_LilyGO_T_Display_S3/tft_config.py')\n",
    "ADD_FILE('tft_buttons.py', '/home/runner/work/MicroPython_LilyGO_T_Display_S3/MicroPython_LilyGO_T_Display_S3/tft_buttons.py')\n",
    "ADD_DIR('examples', '/home/runner/work/MicroPython_LilyGO_T_Display_S3/MicroPython_LilyGO_T_Display_S3/examples')\n"
]

# Escribir el nuevo contenido al manifest
with open(manifest_path, 'w') as file:
    file.writelines(content + new_lines)
