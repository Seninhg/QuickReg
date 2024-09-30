from openpyxl import load_workbook
from openpyxl.styles import Border, Side, Alignment
from datetime import datetime
import os
import json
from scripts.utils import resource_path

# Load the workbook template
template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'plantilla.xlsx')
template_path = resource_path(template_path)

workbook = load_workbook(filename=template_path)

sheet = workbook.active


class GenExcel:
    def __init__(self, checkHandUp = False, salidaTxt = False):
        self.checkHandUp = checkHandUp
        self.salidaTxt = salidaTxt
    def generar(self, nombreCurso, estudiantes):
        #Buscamos información del curso en el archivo JSON
        curso = None
        try:
            path = resource_path(os.path.join(os.path.dirname(__file__), "..", "registros", "courses_reg.json"))
            with open(path, "r") as file:
                data = json.load(file)
                for course in data:
                    if course.get("course_name") == nombreCurso:
                        curso = course
                        break
        except FileNotFoundError:
            print("Error: No se encontró el archivo JSON.")
            return
        if curso is None:
            print(f"Error: No se encontró información del curso {nombreCurso} en el archivo JSON.")
            return
        #-----------ESTILOS
        #estilo de borde
        thin_border = Border(left=Side(style='thin'),
                            right=Side(style='thin'),
                            top=Side(style='thin'),
                            bottom=Side(style='thin'))
        #alinacion de texto
        align_center = Alignment(horizontal='center', vertical='center')
        #-----------INICIALIZACION DE CELDAS
        #celda nombre del curso
        sheet["B4"] = nombreCurso
        #celda profesor
        sheet["B5"] = curso.get("profesor")
        #celda fecha
        now = datetime.now()
        sheet["B6"] = now.strftime("%d/%m/%Y")
        #celda hora
        sheet["B7"] = now.strftime("%H:%M:%S")
        #celda checkHandUp
        sheet["F3"] = "No"
        #celda salida en txt
        sheet["F4"] = "No"
        #--------ITERACION DE ESTUDIANTES
        iterador = 1
        for index, student in enumerate(estudiantes, start=10):
            sheet[f"A{index}"] = iterador
            sheet[f"B{index}"] = student.get("name")
            
            """ 
            MI CODIGO:
            # Si se verifica la mano levantada
            if self.checkHandUp:
                if student.get("attended"):
                    sheet[f"C{index}"] = "A"
                else:
                    sheet[f"C{index}"] = "F"
            else: # Si no se verifica la mano levantada se marca a todos como asistentes
                sheet[f"C{index}"] = "A" """
            # Marcar asistencia dependiendo de si se verifica la mano levantada o no (HUMILLADO POR CHATGPT)
            sheet[f"C{index}"] = "A" if not self.checkHandUp or student.get("attended") else "F"


            # Aplicar bordes a cada celda de la fila
            sheet[f'A{index}'].border = thin_border
            sheet[f'B{index}'].border = thin_border
            sheet[f'C{index}'].border = thin_border

            # Aplicar alineación de texto
            sheet[f'A{index}'].alignment = align_center
            sheet[f'C{index}'].alignment = align_center
    
            iterador += 1

        saveName = nombreCurso.replace(" ", "_") + "(" + now.strftime("%d_%m_%Y_%H") + ").xlsx"
        savePath = os.path.join(os.path.dirname(__file__), "..", "registros", nombreCurso)

        os.makedirs(savePath, exist_ok=True)

        workbook.save(filename=os.path.join(savePath, saveName))