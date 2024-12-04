import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import pandas as pd

class FunctivaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Functiva")
        self.root.geometry("600x600")
        self.create_widgets()

    def create_widgets(self):
        # Título de la aplicación
        self.title_label = tk.Label(self.root, text="Functiva", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=10)

        # Entrada de la función
        self.func_label = tk.Label(self.root, text="Ingrese la función:")
        self.func_label.pack()
        self.func_entry = tk.Entry(self.root, width=50)
        self.func_entry.pack()
        self.func_button = tk.Button(self.root, text="Cargar Función", command=self.cargar_funcion, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.func_button.pack(pady=5)

        # Inputs para valores de a y b
        self.a_label = tk.Label(self.root, text="A:")
        self.a_label.pack()
        self.a_entry = tk.Entry(self.root, width=10)
        self.a_entry.pack()

        self.b_label = tk.Label(self.root, text="B:")
        self.b_label.pack()
        self.b_entry = tk.Entry(self.root, width=10)
        self.b_entry.pack()

        # Selección de tipo de método
        self.method_type_label = tk.Label(self.root, text="Seleccione el tipo de método:")
        self.method_type_label.pack()
        self.method_type_var = tk.StringVar(value="Métodos Abiertos")
        self.method_type_menu = tk.OptionMenu(self.root, self.method_type_var, "Métodos Abiertos", "Métodos Cerrados", command=self.update_method_menu)
        self.method_type_menu.pack()

        # Selección de método específico
        self.method_label = tk.Label(self.root, text="Seleccione el método específico:")
        self.method_label.pack()
        self.method_var = tk.StringVar(value="Newton-Raphson")
        self.method_menu = tk.OptionMenu(self.root, self.method_var, "Newton-Raphson", "Secante")
        self.method_menu.pack()

        # Botón para resolver
        self.solve_func_button = tk.Button(self.root, text="Resolver Función", command=self.resolver_funcion, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.solve_func_button.pack(pady=5)

    def update_method_menu(self, selection):
        # Cambiar el menú de métodos específicos según el tipo
        if selection == "Métodos Abiertos":
            self.method_var.set("Newton-Raphson")
            self.method_menu['menu'].delete(0, 'end')
            self.method_menu['menu'].add_command(label="Newton-Raphson", command=tk._setit(self.method_var, "Newton-Raphson"))
            self.method_menu['menu'].add_command(label="Secante", command=tk._setit(self.method_var, "Secante"))

            # Deshabilitar entradas de a y b
            self.a_label.pack_forget()
            self.a_entry.pack_forget()
            self.b_label.pack_forget()
            self.b_entry.pack_forget()

        elif selection == "Métodos Cerrados":
            self.method_var.set("Bisección")
            self.method_menu['menu'].delete(0, 'end')
            self.method_menu['menu'].add_command(label="Bisección", command=tk._setit(self.method_var, "Bisección"))
            self.method_menu['menu'].add_command(label="Falsa Posición", command=tk._setit(self.method_var, "Falsa Posición"))

            # Habilitar entradas de a y b
            self.a_label.pack()
            self.a_entry.pack()
            self.b_label.pack()
            self.b_entry.pack()

    def cargar_funcion(self):
        funcion_str = self.func_entry.get()
        try:
            self.funcion = parse_expr(funcion_str)
            messagebox.showinfo("Éxito", f"Función cargada correctamente: {self.funcion}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la función: {e}")

    def resolver_funcion(self):
        metodo_principal = self.method_type_var.get()
        metodo_especifico = self.method_var.get()
        
        if hasattr(self, 'funcion'):
            x = sp.symbols('x')
            if metodo_principal == "Métodos Abiertos":
                if metodo_especifico == "Newton-Raphson":
                    self.newton_raphson(self.funcion, x)
                elif metodo_especifico == "Secante":
                    self.secante(self.funcion, x)
            elif metodo_principal == "Métodos Cerrados":
                a = float(self.a_entry.get())
                b = float(self.b_entry.get())
                if metodo_especifico == "Bisección":
                    self.biseccion(self.funcion, x, a, b)
                elif metodo_especifico == "Falsa Posición":
                    self.falsa_posicion(self.funcion, x, a, b)
        else:
            messagebox.showerror("Error", "Primero cargue una función válida.")

#cambio
    def mostrar_iteraciones(self, iteraciones, columnas):
        ventana = Toplevel(self.root)
        ventana.title("Iteraciones")
        ventana.geometry("800x400")

        tree = ttk.Treeview(ventana, columns=columnas, show="headings")
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        for fila in iteraciones:
            tree.insert("", tk.END, values=fila)

        tree.pack(expand=True, fill=tk.BOTH)
        # Métodos numéricos

    # Métodos numéricos
    def newton_raphson(self, funcion, x, tol=1e-6, max_iter=100):
        derivada = sp.diff(funcion, x)
        x0 = 1
        iteraciones = []
        for i in range(max_iter):
            fx = funcion.evalf(subs={x: x0})
            dfx = derivada.evalf(subs={x: x0})
            x1 = x0 - fx / dfx
            error = abs(x1 - x0)
            iteraciones.append([i + 1, x0, fx, dfx, x1, error])
            if error < tol:
                columnas = ["Iteración", "x0", "f(x0)", "f'(x0)", "x1", "Error"]
                self.mostrar_iteraciones(iteraciones, columnas)
                messagebox.showinfo("Resultado", f"Raíz encontrada: {x1}")
                return
            x0 = x1
        messagebox.showerror("Error", "No se encontró raíz con el método Newton-Raphson.")

    def secante(self, funcion, x, tol=1e-6, max_iter=100):
        x0, x1 = 0, 1
        iteraciones = []
        for i in range(max_iter):
            f_x0 = funcion.evalf(subs={x: x0})
            f_x1 = funcion.evalf(subs={x: x1})
            x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
            error = abs(x2 - x1)
            iteraciones.append([i + 1, x0, x1, f_x0, f_x1, x2, error])
            if error < tol:
                columnas = ["Iteración", "x0", "x1", "f(x0)", "f(x1)", "x2", "Error"]
                self.mostrar_iteraciones(iteraciones, columnas)
                messagebox.showinfo("Resultado", f"Raíz encontrada: {x2}")
                return
            x0, x1 = x1, x2
        messagebox.showerror("Error", "No se encontró raíz con el método de la secante.")

    def biseccion(self, funcion, x, a, b, tol=1e-6, max_iter=100):
        iteraciones = []
        if funcion.evalf(subs={x: a}) * funcion.evalf(subs={x: b}) > 0:
            messagebox.showerror("Error", "El intervalo no contiene una raíz.")
            return
        for i in range(max_iter):
            c = (a + b) / 2
            error = abs(b - a) / 2
            iteraciones.append([i + 1, a, b, c, funcion.evalf(subs={x: c}), error])
            if abs(funcion.evalf(subs={x: c})) < tol or error < tol:
                columnas = ["Iteración", "a", "b", "c", "f(c)", "Error"]
                self.mostrar_iteraciones(iteraciones, columnas)
                messagebox.showinfo("Resultado", f"Raíz encontrada: {c}")
                return
            if funcion.evalf(subs={x: a}) * funcion.evalf(subs={x: c}) < 0:
                b = c
            else:
                a = c
        messagebox.showerror("Error", "No se encontró raíz con el método de bisección.")

    def falsa_posicion(self, funcion, x, a, b, tol=1e-6, max_iter=100):
        iteraciones = []
        if funcion.evalf(subs={x: a}) * funcion.evalf(subs={x: b}) > 0:
            messagebox.showerror("Error", "El intervalo no contiene una raíz.")
            return
        for i in range(max_iter):
            fa = funcion.evalf(subs={x: a})
            fb = funcion.evalf(subs={x: b})
            c = b - (fb * (b - a)) / (fb - fa)
            error = abs(funcion.evalf(subs={x: c}))
            iteraciones.append([i + 1, a, b, c, fa, fb, error])
            if error < tol:
                columnas = ["Iteración", "a", "b", "c", "f(a)", "f(b)", "Error"]
                self.mostrar_iteraciones(iteraciones, columnas)
                messagebox.showinfo("Resultado", f"Raíz encontrada: {c}")
                return
            if fa * funcion.evalf(subs={x: c}) < 0:
                b = c
            else:
                a = c
        messagebox.showerror("Error", "No se encontró raíz con el método de falsa posición.")

# Crear la ventana principal de la aplicación
root = tk.Tk()
app = FunctivaApp(root)
root.mainloop()
