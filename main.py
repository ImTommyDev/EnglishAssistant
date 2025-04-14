import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

FILENAME = "english_assistant\\vocabulario.csv"

# Crear archivo CSV si no existe
if not os.path.exists(FILENAME):
    with open(FILENAME, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["english", "spanish", "example_en", "example_es"])

def guardar_linea():
    linea = entry_linea.get()
    partes = [p.strip() for p in linea.split('|')]
    
    if len(partes) != 4:
        messagebox.showerror("Error", "Debe haber 4 elementos separados por '|'.")
        return
    
    with open(FILENAME, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(partes)
    
    entry_linea.delete(0, tk.END)
    messagebox.showinfo("Guardado", f"La palabra '{partes[0]}' fue guardada.")

def buscar_palabra():
    palabra = entry_busqueda.get().lower()
    resultados.delete(*resultados.get_children())

    with open(FILENAME, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if palabra in row["english"].lower():
                resultados.insert("", "end", values=(row["english"], row["spanish"], row["example_en"], row["example_es"]))

def mostrar_prompt():
    texto_prompt = (
        'te voy a pasar una palabra en inglés, quiero que me devuelvas su traduccion al español, '
        'un ejemplo en inglés y la traducción del ejemplo al español, quedará de la siguiente manera, '
        'te paso un ejemplo con la palabra "least":\n'
        'least | menos | she had the least amount of homework today | ella tuvo la menos cantidad de tarea hoy'
    )

    ventana_prompt = tk.Toplevel(ventana)
    ventana_prompt.title("Prompt")
    ventana_prompt.geometry("700x300")
    
    text_widget = tk.Text(ventana_prompt, wrap="word")
    text_widget.insert("1.0", texto_prompt)
    text_widget.config(state="normal")  # editable si quieres permitirlo
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)

    # Botón para cerrar
    tk.Button(ventana_prompt, text="Cerrar", command=ventana_prompt.destroy).pack(pady=5)

# Interfaz
ventana = tk.Tk()
ventana.title("Vocabulario Inglés-Español")

# Centrar ventana al iniciar
w = 800
h = 500
ws = ventana.winfo_screenwidth()
hs = ventana.winfo_screenheight()
x = (ws // 2) - (w // 2)
y = (hs // 2) - (h // 2)
ventana.geometry(f"{w}x{h}+{x}+{y}")

# Hacer que columnas y filas se expandan
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=1)
ventana.rowconfigure(5, weight=1)  # fila de la tabla

# Entrada por línea con '|'
tk.Label(ventana, text="Introduce línea (separada por |):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_linea = tk.Entry(ventana)
entry_linea.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5)

frame_botones = tk.Frame(ventana)
frame_botones.grid(row=2, column=0, columnspan=2, sticky="e", padx=5, pady=5)

tk.Button(frame_botones, text="Guardar línea", command=guardar_linea).pack(side="right", padx=5)
tk.Button(frame_botones, text="Prompt", command=mostrar_prompt).pack(side="right", padx=5)

# Búsqueda
tk.Label(ventana, text="Buscar palabra en inglés:").grid(row=3, column=0, sticky="w", padx=5)
entry_busqueda = tk.Entry(ventana)
entry_busqueda.grid(row=4, column=0, sticky="ew", padx=5)
tk.Button(ventana, text="Buscar", command=buscar_palabra).grid(row=4, column=1, sticky="e", padx=5)

# Tabla de resultados
columnas = ("Inglés", "Español", "Ejemplo Inglés", "Ejemplo Español")
resultados = ttk.Treeview(ventana, columns=columnas, show="headings")
for col in columnas:
    resultados.heading(col, text=col)
    resultados.column(col, width=150, anchor="w")

resultados.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=10)

# Scrollbar para tabla
scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=resultados.yview)
resultados.configure(yscroll=scrollbar.set)
scrollbar.grid(row=5, column=2, sticky="ns")

ventana.mainloop()
# Este código crea una aplicación de escritorio para gestionar vocabulario en inglés y español.
# Permite agregar palabras con ejemplos y buscar palabras en inglés.