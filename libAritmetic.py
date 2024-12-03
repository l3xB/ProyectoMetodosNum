import tkinter as tk
from tkinter import messagebox, Toplevel
import numpy as np
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

        # Labels and Entries for function input
        self.func_label = tk.Label(self.root, text="Ingrese la función:")
        self.func_label.pack()

        self.func_entry = tk.Entry(self.root, width=50)
        self.func_entry.pack()

        self.func_button = tk.Button(self.root, text="Cargar Función", command=self.cargar_funcion, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.func_button.pack(pady=5)

        self.method_type_label = tk.Label(self.root, text="Seleccione el tipo de método:")
        self.method_type_label.pack()

        self.method_type_var = tk.StringVar(value="Métodos Abiertos")
        self.method_type_menu = tk.OptionMenu(self.root, self.method_type_var, "Métodos Abiertos", "Métodos Cerrados", command=self.update_method_menu)
        self.method_type_menu.pack()

        self.method_label = tk.Label(self.root, text="Seleccione el método específico:")
        self.method_label.pack()

        self.method_var = tk.StringVar(value="Newton-Raphson")
        self.method_menu = tk.OptionMenu(self.root, self.method_var, "Newton-Raphson", "Secante")
        self.method_menu.pack()

        self.solve_func_button = tk.Button(self.root, text="Resolver Función", command=self.resolver_funcion, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.solve_func_button.pack(pady=5)

        self.integrate_button = tk.Button(self.root, text="Integrar Función", command=self.integrar_funcion, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.integrate_button.pack(pady=5)

        # Labels and Entries for matrix input
        self.matrix_label = tk.Label(self.root, text="Ingrese la matriz (separada por comas y líneas):")
        self.matrix_label.pack()

        self.matrix_text = tk.Text(self.root, height=5, width=50)
        self.matrix_text.pack()

        self.matrix_button = tk.Button(self.root, text="Cargar Matriz", command=self.cargar_matriz, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"))
        self.matrix_button.pack(pady=5)

        self.solve_button = tk.Button(self.root, text="Resolver Ecuaciones", command=self.resolver_ecuaciones, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"))
        self.solve_button.pack(pady=5)

    def update_method_menu(self, selection):
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

    def cargar_funcion(self):
        funcion_str = self.func_entry.get()
        try:
            self.funcion = parse_expr(funcion_str)
            messagebox.showinfo("Éxito", f"Función cargada correctamente: {self.funcion}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la función: {e}")

    def integrar_funcion(self):
        if hasattr(self, 'funcion'):
            try:
                x = sp.symbols('x')
                integral = sp.integrate(self.funcion, (x, 0, 1))
                self.show_result(f"Integral calculada: {integral}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al integrar la función: {e}")
        else:
            messagebox.showerror("Error", "Primero cargue una función válida.")

    def cargar_matriz(self):
        matriz_str = self.matrix_text.get("1.0", tk.END).strip()
        try:
            matriz = [list(map(float, row.split(','))) for row in matriz_str.split('\n') if row]
            self.matriz = np.array(matriz)
            messagebox.showinfo("Éxito", f"Matriz cargada correctamente: \n{self.matriz}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la matriz: {e}")

    def resolver_ecuaciones(self):
        if hasattr(self, 'matriz'):
            try:
                A = self.matriz[:, :-1]
                b = self.matriz[:, -1]
                solucion = np.linalg.solve(A, b)
                self.show_result(f"Solución de las ecuaciones: {solucion}")
            except np.linalg.LinAlgError as e:
                messagebox.showerror("Error", f"Error al resolver las ecuaciones: {e}")
        else:
            messagebox.showerror("Error", "Primero cargue una matriz válida.")

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
                if metodo_especifico == "Bisección":
                    self.biseccion(self.funcion, x)
                elif metodo_especifico == "Falsa Posición":
                    self.falsa_posicion(self.funcion, x)
        else:
            messagebox.showerror("Error", "Primero cargue una función válida.")

    def newton_raphson(self, funcion, x, tol=1e-6, max_iter=100):
        derivada = sp.diff(funcion, x)
        x0 = 1  # valor inicial arbitrario
        data = {"Iteración": [], "x0": [], "x1": []}
        result_text = "Método Newton-Raphson:\n"
        for i in range(max_iter):
            x1 = x0 - funcion.evalf(subs={x: x0}) / derivada.evalf(subs={x: x0})
            data["Iteración"].append(i+1)
            data["x0"].append(x0)
            data["x1"].append(x1)
            result_text += f"Iteración {i+1}: x0 = {x0}, x1 = {x1}\n"
            if abs(x1 - x0) < tol:
                result_text += f"Raíz encontrada: {x1}\n"
                df = pd.DataFrame(data)
                self.show_result(result_text, df)
                return x1
            x0 = x1
        result_text += "No se encontró raíz con el método Newton-Raphson\n"
        df = pd.DataFrame(data)
        self.show_result(result_text, df)

    def secante(self, funcion, x, tol=1e-6, max_iter=100):
        x0 = 0  # valor inicial arbitrario
        x1 = 1  # segundo valor inicial arbitrario
        data = {"Iteración": [], "x0": [], "x1": [], "x2": []}
        result_text = "Método de la Secante:\n"
        for i in range(max_iter):
            f_x0 = funcion.evalf(subs={x: x0})
            f_x1 = funcion.evalf(subs={x: x1})
            x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
            data["Iteración"].append(i+1)
            data["x0"].append(x0)
            data["x1"].append(x1)
            data["x2"].append(x2)
            result_text += f"Iteración {i+1}: x0 = {x0}, x1 = {x1}, x2 = {x2}\n"
            if abs(x2 - x1) < tol:
                result_text += f"Raíz encontrada: {x2}\n"
                df = pd.DataFrame(data)
                self.show_result(result_text, df)
                return x2
            x0, x1 = x1, x2
        result_text += "No se encontró raíz con el método de la secante\n"
        df = pd.DataFrame(data)
        self.show_result(result_text, df)

    def biseccion(self, funcion, x, a=-1, b=1, tol=1e-6, max_iter=100):
        result_text = "Método de Bisección:\n"
        data = {"Iteración": [], "a": [], "b": [], "c": []}
        if funcion.evalf(subs={x: a}) * funcion.evalf(subs={x: b}) > 0:
            messagebox.showerror("Error", "El intervalo no contiene una raíz")
            return None
        for i in range(max_iter):
            c = (a + b) / 2
            data["Iteración"].append(i+1)
            data["a"].append(a)
            data["b"].append(b)
            data["c"].append(c)
            result_text += f"Iteración {i+1}: a = {a}, b = {b}, c = {c}\n"
            if abs(funcion.evalf(subs={x: c})) < tol or abs(b - a) / 2 < tol:
                result_text += f"Raíz encontrada: {c}\n"
                df = pd.DataFrame(data)
                self.show_result(result_text, df)
                return c
            elif funcion.evalf(subs={x: a}) * funcion.evalf(subs={x: c}) < 0:
                b = c
            else:
                a = c
        result_text += "No se encontró raíz con el método de bisección\n"
        df = pd.DataFrame(data)
        self.show_result(result_text, df)

    def falsa_posicion(self, funcion, x, a=-1, b=1, tol=1e-6, max_iter=100):
        result_text = "Método de Falsa Posición:\n"
        data = {"Iteración": [], "a": [], "b": [], "c": []}
        if funcion.evalf(subs={x: a}) * funcion.evalf(subs={x: b}) > 0:
            messagebox.showerror("Error", "El intervalo no contiene una raíz")
            return None
        for i in range(max_iter):
            c = b - (funcion.evalf(subs={x: b}) * (b - a)) / (funcion.evalf(subs={x: b}) - funcion.evalf(subs={x: a}))
            data["Iteración"].append(i+1)
            data["a"].append(a)
            data["b"].append(b)
            data["c"].append(c)
            result_text += f"Iteración {i+1}: a = {a}, b = {b}, c = {c}\n"
            if abs(funcion.evalf(subs={x: c})) < tol:
                result_text += f"Raíz encontrada: {c}\n"
                df = pd.DataFrame(data)
                self.show_result(result_text, df)
                return c
            elif funcion.evalf(subs={x: a}) * funcion.evalf(subs={x: c}) < 0:
                b = c
            else:
                a = c
        result_text += "No se encontró raíz con el método de falsa posición\n"
        df = pd.DataFrame(data)
        self.show_result(result_text, df)

    def show_result(self, result_text, df):
        result_window = Toplevel(self.root)
        result_window.title("Desarrollo del Proceso")
        result_window.geometry("400x400")
        
        result_output = tk.Text(result_window, wrap=tk.WORD)
        result_output.pack(expand=True, fill='both')
        result_output.insert(tk.END, result_text)
        result_output.config(state=tk.DISABLED)

        save_button = tk.Button(result_window, text="Guardar como Excel", command=lambda: self.save_to_excel(df), bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        save_button.pack(pady=5)
    
    def save_to_excel(self, df):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Éxito", f"Resultados guardados en {file_path}")

# Crear la ventana principal de la aplicación
root = tk.Tk()
app = FunctivaApp(root)
root.mainloop()
