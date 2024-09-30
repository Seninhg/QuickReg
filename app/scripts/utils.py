import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Ejemplo de uso
""" ruta_registro = resource_path('registros/courses_reg.json')
ruta_plantilla = resource_path('templates/plantilla.xlsx') """