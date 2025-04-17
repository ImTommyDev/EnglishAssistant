import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

FILENAME = "vocabulario.csv"

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

    palabra_nueva = partes[0].lower()

    # Verificar si la palabra ya existe
    with open(FILENAME, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["english"].lower() == palabra_nueva:
                messagebox.showwarning("Duplicado", f"La palabra '{partes[0]}' ya existe en el vocabulario.")
                return
    
    # Guardar la nueva línea si no está duplicada
    with open(FILENAME, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(partes)
    
    entry_linea.delete(0, tk.END)
    messagebox.showinfo("Guardado", f"La palabra '{partes[0]}' fue guardada.")
    
    cargar_todas_las_palabras()  # Recargar la tabla después de guardar
def buscar_palabra():
    palabra = entry_busqueda.get().lower()
    resultados.delete(*resultados.get_children())

    with open(FILENAME, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            if palabra in row["english"].lower():
                resultados.insert("", "end", values=(row["english"], row["spanish"], row["example_en"], row["example_es"]), tags=(tag,))

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
def cargar_todas_las_palabras():
    resultados.delete(*resultados.get_children())

    with open(FILENAME, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        filas_ordenadas = sorted(reader, key=lambda x: x["english"].lower())

        for i, row in enumerate(filas_ordenadas):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            resultados.insert("", "end", values=(row["english"], row["spanish"], row["example_en"], row["example_es"]), tags=(tag,))

# Interfaz
ventana = tk.Tk()
ventana.title("Vocabulario Inglés-Español")

fuente_general = ("Segoe UI", 10)
ventana.option_add("*Font", fuente_general)
ventana.option_add("*TButton*highlightBackground", "#4a90e2")
ventana.option_add("*TButton*highlightColor", "#4a90e2")
ventana.option_add("*TButton*highlightThickness", 0)
ventana.option_add("*TButton*borderWidth", 0)
ventana.option_add("*TButton*padding", [5, 5])

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
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=1)


# Entrada de línea
tk.Label(ventana, text="Introduce línea (separada por |):", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 2))
entry_linea = tk.Entry(ventana, relief="solid", borderwidth=1)
entry_linea.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

btn_guardar = tk.Button(ventana, text="Guardar línea", bg="#4a90e2", fg="white", relief="raised", padx=10)
btn_guardar.grid(row=1, column=1, sticky="w", padx=5)

btn_prompt = tk.Button(ventana, text="Prompt", bg="#4a90e2", fg="white", relief="raised", padx=10)
btn_prompt.grid(row=1, column=1, sticky="e", padx=10)
btn_guardar.config(command=guardar_linea)
btn_prompt.config(command=mostrar_prompt)

# Búsqueda
tk.Label(ventana, text="Buscar palabra en inglés:", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky="w", padx=10, pady=(10, 2))
frame_busqueda = tk.Frame(ventana)
frame_busqueda.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
frame_busqueda.columnconfigure(0, weight=1)

entry_busqueda = tk.Entry(frame_busqueda, relief="solid", borderwidth=1)
entry_busqueda.grid(row=0, column=0, sticky="ew")

btn_buscar = tk.Button(frame_busqueda, text="Buscar", bg="#4a90e2", fg="white", relief="raised", padx=10)
btn_buscar.grid(row=0, column=1, padx=(10, 0))
btn_buscar.config(command=buscar_palabra)

# Tabla de resultados
columnas = ("Inglés", "Español", "Ejemplo Inglés", "Ejemplo Español")
resultados = ttk.Treeview(ventana, columns=columnas, show="headings")
anchos_porcentuales = [0.25, 0.25, 0.25, 0.25]  # Distribución equitativa
for col, ancho in zip(columnas, anchos_porcentuales):
    resultados.heading(col, text=col)
    resultados.column(col, anchor="center", stretch=True, width=int(w * ancho))

resultados.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=10)

# Scrollbar para tabla
scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=resultados.yview)
resultados.configure(yscroll=scrollbar.set)
scrollbar.grid(row=5, column=2, sticky="ns")

# Estilo visual más moderno
style = ttk.Style()
style.theme_use("clam")  # Tema moderno

# Encabezados de tabla
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#4a90e2", foreground="white")

# Celdas
style.configure("Treeview", font=("Segoe UI", 10), rowheight=25, background="white", fieldbackground="white")

# Fondo alterno
style.map("Treeview", background=[('selected', '#add8e6')])

# Alternancia de colores en filas
resultados.tag_configure("oddrow", background="#f2f2f2")
resultados.tag_configure("evenrow", background="white")


cargar_todas_las_palabras()
ventana.mainloop()
# Este código crea una aplicación de escritorio para gestionar vocabulario en inglés y español.
# Permite agregar palabras con ejemplos y buscar palabras en inglés.