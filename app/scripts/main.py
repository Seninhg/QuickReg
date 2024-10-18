import openpyxl
import os.path
import datetime
import subprocess
import tkinter as tk
import cv2
from PIL import Image, ImageTk

import util

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+135+130")

        self.login_button_main_window = util.get_button(
            self.main_window,
            "Login",
            "blue",
            self.login
        )
        self.login_button_main_window.place(x=850, y=240)

        self.register_new_user_button_main_window = util.get_button(
            self.main_window,
            "Register",
            "gray92",
            self.register_new_user,
            fg='black'
        )
        self.register_new_user_button_main_window.place(x=850, y=300)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=5, width=850, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        ###self.log_path = './log.txt'


        self.log_path = './log.xlsx'

        if not os.path.exists(self.log_path):
            # Crear el archivo Excel si no existe
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "log"
            ws.append(["Nombre", "Fecha y Hora"])
            wb.save(self.log_path)

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)


    def login(self):

        unknown_img_path = './.tmp.jpg'

        try:
            cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
            output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
            ##print(output)
            name = output.split(',')[1][:-6]
            ##print(name)

            if name in ['no_persons_found', 'unknown_person']:
                util.msg_box('Error', 'Usiario desconocido. '
                                      '\n\nPor favor, REGISTRESE !!! '
                                      '\n\n\n\n\n[Es caso que ya este registrado, intente nuevamente]')
            else:
                util.msg_box('Success !!', 'Bienvenido:  {}'.format(name))

                ##with open(self.log_path, 'a') as f:
                    ##f.write('{} / {}\n'.format(name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    ##f.close()

                self.append_to_log(name)  # Llama a la función que escribe en el log

            os.remove(unknown_img_path)

        except Exception as e:
            util.msg_box('Error', f'Error: {e}')




    def append_to_log(self, name):
        # Abrir el archivo Excel y agregar una nueva fila
        wb = openpyxl.load_workbook(self.log_path)
        ws = wb.active
        ws.append([name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        wb.save(self.log_path)


    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+135+130")

        self.accept_button_register_new_user_window = util.get_button(
            self.register_new_user_window,
            "Accept",
            "blue",
            self.accept_register_new_user
        )
        self.accept_button_register_new_user_window.place(x=870, y=260)

        self.try_again_button_register_new_user_window = util.get_button(
            self.register_new_user_window,
            "Try again",
            "medium sea green",
            self.try_again_register_new_user
        )
        self.try_again_button_register_new_user_window.place(x=870, y=320)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=5, width=850, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=820, y=200)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, "Por favor !!\nIngrese su nombre : ")
        self.text_label_register_new_user.place(x=820, y=130)

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()


    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)

        util.msg_box('Success !!', 'Usuario registrado con exito')

        self.register_new_user_window.destroy()



if __name__ == "__main__":
    app = App()
    app.start()
