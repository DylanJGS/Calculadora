import tkinter as tk
from tkinter import messagebox
import re
from fractions import Fraction


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.geometry("400x500")
        self.config(bg="sky blue")

        # Campo para mostrar ecuaciones y resultados
        self.display = tk.Entry(self, font=("Arial", 24), borderwidth=2, relief="ridge", justify='right')
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        # Botones para la calculadora
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            '', 'CE', '⌫'
        ]

        # Crear botones y asignar 
        for i, button in enumerate(buttons):
            if button == 'CE':
                command = self.clear_display
            elif button == '⌫':
                command = self.backspace
            elif button == '=':
                command = self.calculate
            else:
                command = lambda b=button: self.append_to_expression(b)

            tk.Button(self, text=button, font=("Arial", 18), command=command).grid(
                row=(i // 4) + 1, column=(i % 4), sticky="nsew", padx=10, pady=10)

        # Configuración de columnas y filas
        for i in range(6):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i % 4, weight=1)

        # Asignar para el teclado
        self.bind("<Return>", lambda event: self.calculate())
        self.bind("<KeyPress>", self.on_keypress)
        self.bind("<BackSpace>", lambda event: self.backspace())  

    def append_to_expression(self, char):
        self.display.insert(tk.END, char)

    def clear_display(self):
        self.display.delete(0, tk.END)

    def backspace(self):
        current_text = self.display.get()
        if current_text:
            self.display.delete(len(current_text) - 1, tk.END)

    def calculate(self):
        expression = self.display.get()
        

        # Validar la expresión
        if not re.match(r'^[0-9+*/%.-]+$', expression):
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
            return

        try:
            # Reemplazar fracciones 
            expression = re.sub(r'(\d+)/(\d+)', r'Fraction(\1, \2)', expression)

            
            #convertir el resultado a decimal si es una fracción
            result = eval(expression, {"__builtins__": None}, {"Fraction": Fraction, "abs": abs, "float": float})
            
            #Convertir resultado a decimal
            if isinstance(result, Fraction):
                result = float(result)

            # Mostrar el resultado
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))

        except Exception:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")

    def on_keypress(self, event):
        # Validacion para aceptar solo caracteres
        char = event.char
        if not char.isdigit() and char not in {'.', '/', '*', '-', '+', '%'}:
            messagebox.showwarning("Entrada inválida", "Solo se permiten números y operadores.")


# Iniciar la calculadora
if __name__ == "__main__":
    app = Calculator()
    app.mainloop()