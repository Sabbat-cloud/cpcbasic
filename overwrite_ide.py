import os

new_code = """import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import sys
import re

class CPCIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Amstrad CPC BASIC IDE")
        
        self.root.geometry("800x600")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.editor_frame = tk.Frame(self.main_frame)
        self.editor_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.filename_label = tk.Label(self.editor_frame, text="Sin título", font=("Arial", 10, "bold"), anchor="e")
        self.filename_label.pack(fill=tk.X, pady=(0, 5))

        self.text_area = scrolledtext.ScrolledText(self.editor_frame, wrap=tk.WORD, font=("Courier", 12))
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        self.text_area.bind("<Control-c>", self.copy)
        self.text_area.bind("<Control-v>", self.paste)
        self.text_area.bind("<Control-x>", self.cut)
        self.text_area.bind("<KeyRelease>", self.highlight_syntax)

        self.setup_tags()

        self.current_file = None
        self.process = None

        self.setup_menu()
        
        default_code = '''10 MODE 1
20 PAPER 0
30 PEN 1
40 LOCATE 10, 10
50 PRINT "HOLA DESDE EL IDE!"
60 FOR I=1 TO 5
70 PEN I
80 PRINT "COLOR ", I
90 NEXT I
'''
        self.text_area.insert(tk.END, default_code)
        self.highlight_syntax()

    def setup_tags(self):
        self.text_area.tag_configure("keyword", foreground="blue")
        self.text_area.tag_configure("string", foreground="green")
        self.text_area.tag_configure("comment", foreground="gray")
        self.text_area.tag_configure("number", foreground="darkorange")

    def highlight_syntax(self, event=None):
        for tag in ["keyword", "string", "comment", "number"]:
            self.text_area.tag_remove(tag, "1.0", tk.END)
            
        content = self.text_area.get("1.0", tk.END)
        
        keywords = ["PRINT", "LOCATE", "MODE", "PAPER", "PEN", "FOR", "TO", "STEP", "NEXT", "IF", "THEN", "ELSE", "GOTO", "GOSUB", "RETURN", "DIM", "DATA", "READ", "RESTORE", "INK", "BORDER", "PLOT", "DRAW", "DRAWR", "MOVE", "MOVER", "DEFINT", "DEFREAL", "DEFSTR", "CALL", "ENV", "ENT", "SOUND", "ON", "STOP", "END", "CLS", "CLG", "WINDOW", "INPUT", "WHILE", "WEND", "FILL", "MASK", "GRAPHICS", "TAG", "TAGOFF", "ORIGIN", "DI", "EI", "REM", "CLEAR", "SYMBOL", "ABS", "ASC", "CHR\$", "CINT", "COS", "CREAL", "EXP", "FIX", "INT", "LEFT\$", "LEN", "LOG", "LOG10", "LOWER\$", "MID\$", "PI", "POS", "RIGHT\$", "RND", "SGN", "SIN", "SPACE\$", "SQ", "SQR", "STR\$", "STRING\$", "TAN", "TEST", "TESTR", "TIME", "UNT", "UPPER\$", "VAL", "VPOS", "XPOS", "YPOS", "INKEY", "INKEY\$", "JOY", "PEEK", "ROUND"]
        kw_pattern = r"\\b(" + "|".join(keywords) + r")\\b"
        
        patterns = {
            "string": r'".*?"',
            "comment": r"('.*|\\bREM\\b.*)",
            "keyword": kw_pattern,
            "number": r"\\b\\d+\\b"
        }
        
        for tag, pattern in patterns.items():
            for match in re.finditer(pattern, content, re.IGNORECASE):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.text_area.tag_add(tag, start, end)

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_command(label="Guardar Como...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.on_closing)
        menubar.add_cascade(label="Archivo", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Copiar", command=self.copy)
        edit_menu.add_command(label="Pegar", command=self.paste)
        edit_menu.add_command(label="Cortar", command=self.cut)
        menubar.add_cascade(label="Edición", menu=edit_menu)

        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="Ejecutar (F5)", command=self.run_code)
        run_menu.add_command(label="Detener (F6)", command=self.stop_code)
        menubar.add_cascade(label="Ejecutar", menu=run_menu)

        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Paleta de Colores", command=self.show_colors)
        tools_menu.add_command(label="Tabla ASCII", command=self.show_ascii)
        tools_menu.add_command(label="Guía de Coordenadas", command=self.show_coords)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        
        self.root.config(menu=menubar)
        
        self.root.bind('<F5>', lambda e: self.run_code())
        self.root.bind('<F6>', lambda e: self.stop_code())
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_colors(self):
        win = tk.Toplevel(self.root)
        win.title("Paleta de Colores CPC")
        win.geometry("400x400")
        text = scrolledtext.ScrolledText(win, font=("Courier", 10))
        text.pack(fill=tk.BOTH, expand=True)
        colors = \"\"\"Colores Hardware Amstrad CPC:

0  Negro             14 Naranja Pastel
1  Azul              15 Naranja
2  Azul Brillante    16 Rojo Rosa
3  Rojo              17 Violeta Pastel
4  Magenta           18 Verde Brillante
5  Malva             19 Verde Mar Brill.
6  Rojo Brillante    20 Cian Brillante
7  Púrpura           21 Verde Lima
8  Magenta Brillante 22 Verde Pastel
9  Verde             23 Cian Pastel
10 Cian              24 Amarillo Brill.
11 Azul Cielo        25 Amarillo Pastel
12 Amarillo          26 Blanco Brillante
13 Blanco

Nota: En Locomotive BASIC (INK, PAPER, PEN) 
se usan los IDs lógicos. Por defecto, las
tintas lógicas están mapeadas a colores 
hardware.
\"\"\"
        text.insert(tk.END, colors)
        text.config(state=tk.DISABLED)

    def show_ascii(self):
        win = tk.Toplevel(self.root)
        win.title("Tabla ASCII")
        win.geometry("300x500")
        text = scrolledtext.ScrolledText(win, font=("Courier", 10))
        text.pack(fill=tk.BOTH, expand=True)
        ascii_table = \"\"\"Tabla de caracteres (selección):

Control:
 7  BEL (Beep)
 8  BS  (Backspace / Izquierda)
 9  TAB (Avanza cursor)
 10 LF  (Baja cursor)
 11 VT  (Sube cursor)
 12 FF  (Limpia ventana)
 13 CR  (Cursor al principio)
 24 CAN (Invierte tinta y fondo)

ASCII Imprimible:
 32 [Espacio]
 33 !    34 \"    35 #
 36 $    37 %    38 &
 39 '    40 (    41 )
 42 *    43 +    44 ,
 45 -    46 .    47 /
 48 0 .. 57 9
 58 :    59 ;    60 <
 61 =    62 >    63 ?
 64 @
 65 A .. 90 Z
 91 [    92 \    93 ]
 94 ^    95 _    96 `
 97 a .. 122 z
123 {    124 |   125 }
126 ~
\"\"\"
        text.insert(tk.END, ascii_table)
        text.config(state=tk.DISABLED)

    def show_coords(self):
        win = tk.Toplevel(self.root)
        win.title("Guía de Coordenadas Gráficas")
        win.geometry("500x350")
        text = scrolledtext.ScrolledText(win, font=("Courier", 10))
        text.pack(fill=tk.BOTH, expand=True)
        coords = \"\"\"Sistema de Coordenadas Gráficas (CPC):

Resolución virtual (todos los MODEs):
  X: 0 a 640 (de izquierda a derecha)
  Y: 0 a 400 (de abajo hacia arriba)

ORIGEN por defecto (0, 0):
  Esquina inferior izquierda.
  * Ojo: En algunos ordenadores es la
    superior izquierda, pero en el CPC
    el eje Y sube hacia arriba.

MODEs de Video:
  MODE 0: 160x200 (16 colores)
    El píxel es muy ancho. 
    1 unidad X = 4 píxeles gráficos.

  MODE 1: 320x200 (4 colores)
    El píxel es normal.
    1 unidad X = 2 píxeles gráficos.

  MODE 2: 640x200 (2 colores)
    Alta resolución (ideal texto).
    1 unidad X = 1 píxel gráfico.

Uso de TAG / TAGOFF:
  TAG activa el cursor gráfico para texto,
  permitiendo PRINT en coordenadas 
  gráficas (ej. PRINT CHR$(24) en x, y).
\"\"\"
        text.insert(tk.END, coords)
        text.config(state=tk.DISABLED)

    def copy(self, event=None):
        try:
            text = self.text_area.get("sel.first", "sel.last")
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
        except tk.TclError:
            pass
        return "break" if event else None

    def paste(self, event=None):
        try:
            text = self.root.clipboard_get()
            self.text_area.insert(tk.INSERT, text)
            self.highlight_syntax()
        except tk.TclError:
            pass
        return "break" if event else None

    def cut(self, event=None):
        self.copy()
        try:
            self.text_area.delete("sel.first", "sel.last")
            self.highlight_syntax()
        except tk.TclError:
            pass
        return "break" if event else None

    def _update_filename_label(self):
        if self.current_file:
            self.filename_label.config(text=os.path.basename(self.current_file))
        else:
            self.filename_label.config(text="Sin título")

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self._update_filename_label()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos BASIC", "*.cpcbas *.bas"), ("Todos los archivos", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, f.read())
                self.current_file = file_path
                self._update_filename_label()
                self.highlight_syntax()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as f:
                    f.write(self.text_area.get(1.0, tk.END))
                self._update_filename_label()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".cpcbas", filetypes=[("Archivos BASIC", "*.cpcbas *.bas"), ("Todos los archivos", "*.*")])
        if file_path:
            self.current_file = file_path
            self.save_file()
            self._update_filename_label()

    def run_code(self):
        self.stop_code()
        
        code = self.text_area.get(1.0, tk.END)
        temp_file = os.path.join(os.path.dirname(__file__), "temp_run.cpcbas")
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(code)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear archivo temporal:\n{e}")
            return

        env = os.environ.copy()
        
        main_py = os.path.join(os.path.dirname(__file__), "main.py")
        
        try:
            # We don't pass SDL_WINDOWID anymore so Pygame opens a new interactive window
            self.process = subprocess.Popen([sys.executable, main_py, temp_file, "--scale", "2"], env=env)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar el emulador:\n{e}")

    def stop_code(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None

    def on_closing(self):
        self.stop_code()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CPCIDE(root)
    root.mainloop()
"""

with open('ide.py', 'w', encoding='utf-8') as f:
    f.write(new_code)
