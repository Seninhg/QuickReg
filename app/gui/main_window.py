import tkinter as tk
from tkinter import ttk, filedialog
from gui.registrar_curso import RegistrarCurso
from gui.utils_window import UtilsWindow
from scripts.ocr import ScanearCaptura
from scripts.utils import resource_path
import os
import json
from pathlib import Path
import shutil


class QuickRegApp:
    def __init__(self, root):
        self.utilsWindow = UtilsWindow(root)
        # Configuración básica de la ventana
        root.title("QuickReg")
        root.geometry("750x300") 
        bgColorGeneral = "#C08922" #6F8E85
        root.configure(bg=bgColorGeneral)
        root.resizable(False, False)

        ##EVENTOS
        root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(root))

        #ruta temporal para las imagenes
        self.rutaTemporal = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "temp"))
        self.rutaTemporal = resource_path(self.rutaTemporal)
        self.createFolder(self.rutaTemporal)

        """
            ALGUNOS COLORES
        """
        bgButtonPrimary = "#2C2C2C"


        #contEncabezado
        self.contEncabezado = tk.Frame(root, bg="#351B1B")
        self.contEncabezado.pack(fill="both", expand=True)
        # Título
        self.title_label = tk.Label(self.contEncabezado, text="Registro de estudiantes con IA", font=("Helvetica", 20, "bold"), bg="#351B1B", fg="white")
        self.title_label.pack(pady=10)

        # Marco principal que contendrá los bloques izquierdo, derecho e inferior
        self.main_frame = tk.Frame(root, bg="#6F784C")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)        
        
        bgColorLeft = "#6F784C"
        # Bloque izquierdo
        self.left_frame = tk.Frame(self.main_frame, bg=bgColorLeft)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=10)
        
        bgColorRight = "#6F784C"
        # Bloque derecho
        self.right_frame = tk.Frame(self.main_frame, bg=bgColorRight)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)

        # Bloque inferior
        self.bottom_frame = tk.Frame(root, bg=bgColorGeneral)
        self.bottom_frame.pack(fill="both", expand=True)

        # Configuración de expansión de los bloques
        self.main_frame.columnconfigure(0, weight=1)  # El bloque izquierdo se expande proporcionalmente
        self.main_frame.columnconfigure(1, weight=1)  # El bloque derecho se expande proporcionalmente
        self.main_frame.rowconfigure(0, weight=1)     # Bloques izquierdo y derecho expandibles
        self.main_frame.rowconfigure(1, weight=0)     # El bloque inferior no se expande

        #----------------- Contenido del bloque izquierdo-----------------
        """FILA 1"""
        self.row1_block1 = tk.Frame(self.left_frame, bg=bgColorLeft)
        self.row1_block1.grid(row=0, column=0, sticky="w", pady=10)

        # Etiqueta y combobox para seleccionar el curso
        self.course_label = tk.Label(self.row1_block1, text="Curso:", font=("Helvetica", 12), bg=bgColorLeft, anchor="w")
        self.course_label.grid(row=0, column=0, sticky="w", padx=5)
        
        self.courses = ["Seleccionar curso"]        

        self.course_combobox = ttk.Combobox(self.row1_block1, values=self.courses, state="readonly")
        self.course_combobox.current(0)
        self.course_combobox.grid(row=0, column=1, padx=5)


        
        self.actualizar_combobox()

        # Botón para registrar un nuevo curso
        self.register_course_button = tk.Button(self.row1_block1, text="Registrar curso", bg=bgButtonPrimary, fg="white", command=lambda: RegistrarCurso(root, self.actualizar_combobox))
        self.register_course_button.grid(row=0, column=2, padx=10)

        self.hoverEffect(self.register_course_button)

        """FILA 2"""
        self.row2_block1 = tk.Frame(self.left_frame, bg=bgColorLeft)
        self.row2_block1.grid(row=1, column=0, sticky="w", pady=10)

        self.capture_label = tk.Label(self.row2_block1, text="Captura de pantalla:", font=("Helvetica", 12), bg=bgColorLeft)
        self.capture_label.grid(row=0, column=0, sticky="w", padx=5)

        self.select_file_button = tk.Button(self.row2_block1, text="📎", command=self.select_file, font=("Helvetica", 20), padx=0, pady=0, borderwidth=0, background=bgColorLeft)
        self.select_file_button.grid(row=0, column=1)

        self.hoverEffect(self.select_file_button)


        self.filepath_entry = tk.Entry(self.row2_block1, width=30)
        self.filepath_entry.grid(row=0, column=2, padx=10)

        self.capture_button = tk.Button(self.row2_block1, text="Hacer captura", fg="white",  bg=bgButtonPrimary,state=tk.DISABLED)
        self.capture_button.grid(row=1, column=2, pady=10, sticky="w")

        self.hoverEffect(self.capture_button)


        # ----------------------------------Contenido del bloque derecho--------------------------------
        self.row1_block2 = tk.Frame(self.right_frame, bg=bgColorRight)
        self.row1_block2.grid(row=0, column=0, sticky="nsew", pady=10)

        # Checkbutton para verificar asistencia
        self.verify_var = tk.BooleanVar()
        self.verify_checkbox = tk.Checkbutton(self.row1_block2, text="Verificar asistencia", variable=self.verify_var, bg=bgColorRight, state=tk.DISABLED)
        self.verify_checkbox.grid(row=0, column=0, sticky="w", padx=5)

        self.hoverEffect(self.verify_checkbox)

        # Combobox para seleccionar el método de verificación
        self.method_combobox = ttk.Combobox(self.row1_block2, values=["Mano levantada", "Cámara encendida"], state="readonly")
        self.method_combobox.current(0)
        self.method_combobox.grid(row=0, column=1, padx=10)


        # Checkbutton para obtener txt
        self.ocr_var = tk.BooleanVar()
        self.ocr_checkbox = tk.Checkbutton(self.row1_block2, text="Obtener txt", fg="black", variable=self.ocr_var, bg=bgColorRight, state=tk.DISABLED)
        self.ocr_checkbox.grid(row=1, column=0, sticky="w", padx=5)
        
        self.hoverEffect(self.ocr_checkbox)

        """
        Parte inferior
        """
        # Contenedor para centrar los botones
        self.button_container = tk.Frame(self.bottom_frame, bg=bgColorGeneral)
        self.button_container.pack(expand=True)

        self.register_button = tk.Button(self.button_container, text="Registrar asistencia", bg=bgButtonPrimary, fg="white", command=self.register_btn)
        self.register_button.pack(side=tk.LEFT)

        self.hoverEffect(self.register_button)

        # Icono clickeable
        self.icon_button = tk.Button(self.button_container, text="📁", font=("Helvetica", 18), padx=0, pady=0, bg=bgColorGeneral, fg="white", borderwidth=0, command= lambda: self.openFolder("registros"))
        self.icon_button.pack(side=tk.LEFT)

        self.hoverEffect(self.icon_button)
    
    def openFolder(self, folder):
        """
            * El path debe ser relativa a la ruta de la aplicación
        """
        try:
            path = resource_path(os.path.join(os.path.dirname(__file__), "..", folder))
            os.startfile(path)
        except FileNotFoundError:
            self.utilsWindow.popUp("error", message=f"El directorio {folder} no existe.")
        except Exception as e:
            self.utilsWindow.popUp("error", "error desconocido", f"Al parecer hubo un problema {e}")
        
    def hoverEffect(self, widget):
        if widget.cget("state") != tk.DISABLED:
            widget.bind("<Enter>", lambda e: widget.config(cursor="hand2"))
            widget.bind("<Leave>", lambda e: widget.config(cursor=""))

    def actualizar_combobox(self):
        self.courses.clear()
        self.courses.append("Seleccionar curso")
        #cargamos valores para el combobox
        pathApp = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        pathApp = resource_path(pathApp)
        pathJson = os.path.join(pathApp, "registros", "courses_reg.json")
        try:
            with open(pathJson, "r") as file:
                data = json.load(file)
                for course in data:
                    self.courses.append(course["course_name"])
                self.course_combobox["values"] = self.courses
                self.course_combobox.current(0)
        except FileNotFoundError:
            print(f"Error: El archivo {pathJson} no existe.")
        except json.JSONDecodeError:
            print("Error: El archivo JSON está malformado.")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def select_file(self):
        # Abrir diálogo para seleccionar archivo
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.filepath_entry.delete(0, tk.END)
            self.filepath_entry.insert(0, file_path)
        
    def register_btn(self):
        """
        Método para registrar la asistencia haciendo uso de la captura de pantalla y demás parámetros seleccionados
        """
        #ruta de imagen
        pathImage = Path(self.filepath_entry.get())
        #nombre del curso
        courseName = self.course_combobox.get()
        #metodo de verificación
        check_verifyAssis = self.verify_var.get()
        method = self.method_combobox.get()
        #obtener txt
        check_getTxt = self.ocr_var.get()

        if pathImage and courseName != "Seleccionar curso":
            scanearCaptura = ScanearCaptura(courseName, check_verifyAssis)

            if pathImage.exists() and pathImage.is_file():
                #ubicación temporal para la imagen
                shutil.copy(pathImage, self.rutaTemporal)
                pathImage = os.path.join(self.rutaTemporal, pathImage.name)
            else:
                self.utilsWindow.popUp("error", "Error", "No se pudo cargar la imagen. Comprueba que la ruta sea correcta. Esto puede deberse al uso de caracteres especiales en la ruta del archivo.")
                return

            result = scanearCaptura.getStudents(pathImage)
            
            if result["status"] == "success":
                self.utilsWindow.popUp("info", "Asistencia registrada", result["message"])
            else:
                self.utilsWindow.popUp("error", "Error", result["message"])
        else:
            self.utilsWindow.popUp("error", "Error", "Por favor, complete todos los campos. (Curso y captura de pantalla)")

    def on_closing(self, root):
        response = self.utilsWindow.popUp("question", "Salir", "¿Estás seguro que deseas salir?")
        if response == "yes":
            if os.path.exists(self.rutaTemporal):
                shutil.rmtree(self.rutaTemporal)
                print("Directorio temporal eliminado.")
            root.destroy()
    
    def createFolder(self, path):
        """
            * Crea una carpeta en la ruta especificada
        """
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except FileExistsError:
            pass
        except Exception as e:
            self.utilsWindow.popUp("error", "Error", f"Error inesperado: {e}")