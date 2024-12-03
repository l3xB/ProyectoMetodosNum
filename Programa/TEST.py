#arreglar metodos abiertos y cerrados:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#matriz inversa funciona bien
import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import subprocess  # Asegúrate de incluir esto al inicio del archivo

class FunctivaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Functiva")
        self.root.geometry("600x600")
        self.root.configure(bg="lightblue")
        self.create_widgets()

    def create_widgets(self):
        # Título de la aplicación
        self.title_label = tk.Label(self.root, text="Functiva", font=("Helvetica", 24, "bold"), bg="lightblue")
        self.title_label.pack(pady=10)

        self.integrate_button = tk.Button(self.root, text="Solución por Matrices", command=self.Matriz, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.integrate_button.pack(pady=5)

        self.integrate_button = tk.Button(self.root, text="Solución por Integración", command=self.integrar_funcion, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.integrate_button.pack(pady=5)


        self.integrate_button = tk.Button(self.root, text="Solución por Metodos Abiertos y Cerrados", command=self.Metodos_abiertos_cerrados, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.integrate_button.pack(pady=5)

        # Labels and Entries for matrix input

        #ttk.Separator(self.root, orient=tk.HORIZONTAL).place(relx=0, rely=0.76, relheight=1, relwidth=1) 
        

    def update_method_menu(self, selection):
        # Cambiar el menú de métodos según el tipo seleccionado
        if selection == "Métodos Abiertos":
            self.method_var.set("Newton-Raphson")
            self.method_menu['menu'].delete(0, 'end')
            self.method_menu['menu'].add_command(label="Newton-Raphson", command=tk._setit(self.method_var, "Newton-Raphson"))
            self.method_menu['menu'].add_command(label="Secante", command=tk._setit(self.method_var, "Secante"))
        elif selection == "Métodos Cerrados":
            self.method_var.set("Bisección")
            self.method_menu['menu'].delete(0, 'end')
            self.method_menu['menu'].add_command(label="Bisección", command=tk._setit(self.method_var, "Bisección"))
            self.method_menu['menu'].add_command(label="Falsa Posición", command=tk._setit(self.method_var, "Falsa Posición"))

    

    def Metodos_abiertos_cerrados(self):
        try:
            subprocess.Popen(["python", "METODOSAB.py"])  # Cambia 'segundo_archivo.py' por el nombre de tu archivo
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'segundo_archivo.py'. Verifica su ubicación.") 
    

    def integrar_funcion(self):
        try:
            subprocess.Popen(["python", "INTEGRAR.py"])  # Cambia 'segundo_archivo.py' por el nombre de tu archivo
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'segundo_archivo.py'. Verifica su ubicación.")

    def Matriz(self):
        try:
            subprocess.Popen(["python", "MATRIZ.py"])  # Cambia 'segundo_archivo.py' por el nombre de tu archivo
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'segundo_archivo.py'. Verifica su ubicación.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FunctivaApp(root)
    root.mainloop()