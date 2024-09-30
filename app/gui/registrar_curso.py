import tkinter as tk
from tkinter import ttk
from gui.utils_window import UtilsWindow
import os
import json
from scripts.utils import resource_path


class RegistrarCurso:
    def __init__(self, root, actualizar_combobox):

        self.utilsWindow = UtilsWindow(root)
        # Crear la ventana modal
        self.window = tk.Toplevel(root)
        self.window.title("Registrar nuevo curso")
        self.window.geometry("400x250")
        bgColor = "#F4EEDA"
        self.window.configure(bg=bgColor)
        self.window.resizable(False, False)

        #función para actualizar el combobox de la ventana principal
        self.actualizar_cursos = actualizar_combobox

        # Título
        self.title_label = tk.Label(self.window, text="Registrar nuevo curso", font=("Helvetica", 14, "bold"), bg=bgColor)
        self.title_label.pack(pady=10)

        # Marco principal para los campos del formulario
        self.form_frame = tk.Frame(self.window, bg=bgColor)
        self.form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Nombre del curso
        self.course_name_label = tk.Label(self.form_frame, text="Nombre del curso: (evite el uso de caracteres especiales)", font=("Helvetica", 10), bg=bgColor)
        self.course_name_label.grid(row=0, column=0, sticky="w", pady=5)
        
        self.course_name_entry = tk.Entry(self.form_frame, width=30)
        self.course_name_entry.grid(row=1, column=0, pady=5)

        # Profesor a cargo
        self.professor_name_label = tk.Label(self.form_frame, text="Profesor a cargo:", font=("Helvetica", 10), bg=bgColor)
        self.professor_name_label.grid(row=2, column=0, sticky="w", pady=5)
        
        self.professor_name_entry = tk.Entry(self.form_frame, width=30)
        self.professor_name_entry.grid(row=3, column=0, pady=5)

        # Botón para agregar curso
        self.add_course_button = tk.Button(self.window, text="Agregar curso", bg="#4E4A4A", fg="white", command=self.add_course)
        self.add_course_button.pack(pady=10)

    def add_course(self):
        # Acción para el botón "Agregar curso"
        course_name = self.course_name_entry.get()
        professor_name = self.professor_name_entry.get()
        
        if course_name and professor_name:
            pathApp = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            pathApp = resource_path(pathApp)
            # Registramos el curso en el archivo JSON
            pathJson = os.path.join(pathApp, "registros", "courses_reg.json")
            try:
                with open(pathJson, "r") as file:
                    data = json.load(file)
                    lastId = data[-1]["course_id"] if data else 0
                    new_course = {"course_id": lastId + 1, "course_name": course_name, "profesor": professor_name}
                    data.append(new_course)
                with open(pathJson, "w") as file:
                    json.dump(data, file, indent=4)
                    self.utilsWindow.popUp(alert_type='info', title='Curso registrado', message='El curso se ha registrado correctamente.')
            except FileNotFoundError:
                print(f"Error: El archivo {pathJson} no existe.")
            except json.JSONDecodeError:
                print("Error: El archivo JSON está malformado.")
            except Exception as e:
                print(f"Error inesperado: {e}")
            #creamos carpeta para el curso
            pathCourse = os.path.join(pathApp, "registros", course_name)
            try:
                os.makedirs(pathCourse)
                self.utilsWindow.popUp(alert_type='info', title='Curso registrado', message='Se ha creado una carpeta para el curso.')
            except FileExistsError:
                self.utilsWindow.popUp(alert_type='warning', title='Curso existente', message='El curso ya se encuentra registrado.')
            except Exception as e:
                self.utilsWindow.popUp(alert_type='error', title='Error', message=f'Error inesperado: {e}')

            self.actualizar_cursos()  # Actualizar el combobox de la ventana principal
            self.window.destroy()  # Cerrar la ventana modal después de registrar el curso
        else:
            self.utilsWindow.popUp(alert_type='warning', title='Campos vacíos', message='Por favor, completa todos los campos.')

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrarCurso(root)
    root.mainloop()
