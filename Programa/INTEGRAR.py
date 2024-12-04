#regla 3/8 bien 
#regla 1/3
#regla boole 
#regla trapecio

import tkinter as tk
from tkinter import messagebox, ttk
import sympy as sp


class IntegrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos de Integración")
        self.root.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        # Título
        tk.Label(self.root, text="Métodos de Integración", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Entrada de la función
        tk.Label(self.root, text="Ingrese la función f(x):").pack()
        self.func_entry = tk.Entry(self.root, width=50)
        self.func_entry.pack(pady=5)

        # Entrada del límite inferior a
        tk.Label(self.root, text="Ingrese el valor de a (límite inferior):").pack()
        self.a_entry = tk.Entry(self.root, width=20)
        self.a_entry.pack(pady=5)

        # Entrada del límite superior b
        tk.Label(self.root, text="Ingrese el valor de b (límite superior):").pack()
        self.b_entry = tk.Entry(self.root, width=20)
        self.b_entry.pack(pady=5)

        # Selección del método
        tk.Label(self.root, text="Seleccione el método:").pack()
        self.method_var = tk.StringVar(value="Trapecio")
        self.method_menu = ttk.Combobox(
            self.root,
            textvariable=self.method_var,
            values=["Trapecio", "Simpson 1/3", "Simpson 3/8", "Regla de Boole"],
            state="readonly"
        )
        self.method_menu.pack(pady=5)

        # Botón para calcular
        tk.Button(self.root, text="Calcular", command=self.calcular_integral, bg="#4CAF50", fg="white").pack(pady=10)

    def calcular_integral(self):
        try:
            # Leer entradas
            funcion_str = self.func_entry.get()
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            metodo = self.method_var.get()

            # Convertir la función en una expresión simbólica
            x = sp.Symbol('x')
            funcion = sp.lambdify(x, sp.sympify(funcion_str), 'numpy')

            # Realizar el cálculo según el método
            if metodo == "Trapecio":
                resultado = self.trapecio(funcion, a, b)
            elif metodo == "Simpson 1/3":
                resultado = self.simpson_1_3(funcion, a, b)
            elif metodo == "Simpson 3/8":
                resultado = self.simpson_3_8(funcion, a, b)
            elif metodo == "Regla de Boole":
                resultado = self.boole(funcion, a, b)
            else:
                raise ValueError("Método no reconocido")

            # Mostrar resultado
            messagebox.showinfo("Resultado", f"El resultado de la integral es: {resultado:.6f}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la integral: {e}")

    def trapecio(self, f, a, b):
        return (b - a) * (f(a) + f(b)) / 2

    def simpson_1_3(self, f, a, b):
        mid = (a + b) / 2
        return (b - a) / 6 * (f(a) + 4 * f(mid) + f(b))

    def simpson_3_8(self, f, a, b):
        h = (b - a) / 3
        return 3 * h / 8 * (f(a) + 3 * f(a + h) + 3 * f(a + 2 * h) + f(b))

    def boole(self, f, a, b):
        h = (b - a) / 4
        return 2 * h / 45 * (7 * f(a) + 32 * f(a + h) + 12 * f(a + 2 * h) + 32 * f(a + 3 * h) + 7 * f(b))


if __name__ == "__main__":
    root = tk.Tk()
    app = IntegrationApp(root)
    root.mainloop()
