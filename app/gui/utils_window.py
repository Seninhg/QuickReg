import tkinter as tk
from tkinter import messagebox

class UtilsWindow:
    def __init__(self, root):
        self.root = root

    def popUp(self, alert_type='info', title='Alerta', message='Este es un mensaje de alerta'):
        # Determinar el tipo de alerta a mostrar
        if alert_type == 'info':
            messagebox.showinfo(title, message)
        elif alert_type == 'warning':
            messagebox.showwarning(title, message)
        elif alert_type == 'error':
            messagebox.showerror(title, message)
        elif alert_type == 'question':
            response = messagebox.askquestion(title, message)
            print('Respuesta:', response)
        else:
            messagebox.showinfo(title, message)