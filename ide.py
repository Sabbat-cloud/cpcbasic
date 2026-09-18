import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import sys

class CPCIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Amstrad CPC BASIC IDE")
        
        # 704x464 for scale 1 (640x400 + 32 logical border)
        self.root.geometry("1170x520")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.emu_frame = tk.Frame(self.main_frame, width=704, height=464, bg="black")
        self.emu_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.NONE, expand=False)
        self.emu_frame.pack_propagate(False)

        self.editor_frame = tk.Frame(self.main_frame)
        self.editor_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.text_area = scrolledtext.ScrolledText(self.editor_frame, wrap=tk.WORD, font=("Courier", 12))
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        self.text_area.bind("<Control-c>", self.copy)
        self.text_area.bind("<Control-v>", self.paste)
        self.text_area.bind("<Control-x>", self.cut)

        self.current_file = None
        self.process = None

        self.setup_menu()
        
        default_code = """10 MODE 1
20 PAPER 0
30 PEN 1
40 LOCATE 10, 10
50 PRINT "HOLA DESDE EL IDE!"
60 FOR I=1 TO 5
70 PEN I
80 PRINT "COLOR ", I
90 NEXT I
"""
        self.text_area.insert(tk.END, default_code)

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
        
        self.root.config(menu=menubar)
        
        self.root.bind('<F5>', lambda e: self.run_code())
        self.root.bind('<F6>', lambda e: self.stop_code())
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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
        except tk.TclError:
            pass
        return "break" if event else None

    def cut(self, event=None):
        self.copy()
        try:
            self.text_area.delete("sel.first", "sel.last")
        except tk.TclError:
            pass
        return "break" if event else None

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos BASIC", "*.cpcbas *.bas"), ("Todos los archivos", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, f.read())
                self.current_file = file_path
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as f:
                    f.write(self.text_area.get(1.0, tk.END))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".cpcbas", filetypes=[("Archivos BASIC", "*.cpcbas *.bas"), ("Todos los archivos", "*.*")])
        if file_path:
            self.current_file = file_path
            self.save_file()

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
        env['SDL_WINDOWID'] = str(self.emu_frame.winfo_id())
        
        # En Windows a veces es necesario especificar el driver SDL
        if sys.platform == 'win32':
            env['SDL_VIDEODRIVER'] = 'windows'

        main_py = os.path.join(os.path.dirname(__file__), "main.py")
        
        try:
            self.process = subprocess.Popen([sys.executable, main_py, temp_file, "--scale", "1"], env=env)
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
