import sys
import os
import threading
import queue

if sys.platform == 'win32':
    os.environ['SDL_AUDIODRIVER'] = 'directsound'

import pygame
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()

import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from core.lexer import Lexer
from core.parser import Parser
from core.interpreter import Interpreter
from core.storage import DSKManager

class EmulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Amstrad CPC Emulator Control")
        self.root.geometry("600x500")

        self.interpreter = Interpreter(None, scale=2, speed='unlimited')
        self.interpreter.running = True
        
        self.repl_queue = queue.Queue()
        self.setup_menu()
        self.setup_ui()

        self.dsk = None
        self.exec_thread = threading.Thread(target=self.emulator_thread_loop, daemon=True)
        self.exec_thread.start()

        # Auto-load midisco.dsk if exists
        if os.path.exists('midisco.dsk'):
            self.dsk = DSKManager('midisco.dsk')
            if self.dsk.mount():
                self.interpreter.dsk = self.dsk

        self.update_gui()

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Abrir Archivo...", command=self.open_file)
        file_menu.add_command(label="Guardar Archivo Como...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Cargar DSK...", command=self.load_dsk)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)

        run_menu = tk.Menu(menubar, tearoff=0)
        self.speed_var = tk.StringVar(value='unlimited')
        run_menu.add_radiobutton(label="Velocidad: Ilimitada", variable=self.speed_var, value='unlimited', command=self.update_speed)
        run_menu.add_radiobutton(label="Velocidad: Real (CPC 6128)", variable=self.speed_var, value='real', command=self.update_speed)
        menubar.add_cascade(label="Ejecutar", menu=run_menu)

        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Paleta de Colores", command=self.show_colors)
        tools_menu.add_command(label="Tabla ASCII", command=self.show_ascii)
        tools_menu.add_command(label="Guía de Coordenadas", command=self.show_coords)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        
        self.root.config(menu=menubar)

    def setup_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tab_z80 = ttk.Frame(notebook)
        notebook.add(self.tab_z80, text="Z80 CPU")
        self.reg_vars = {}
        regs = ['A', 'F', 'B', 'C', 'D', 'E', 'H', 'L', 'PC', 'SP']
        for i, reg in enumerate(regs):
            ttk.Label(self.tab_z80, text=f"{reg}:", font=("Courier", 12, "bold")).grid(row=i//2, column=(i%2)*2, padx=10, pady=5, sticky='e')
            var = tk.StringVar(value="00")
            ttk.Label(self.tab_z80, textvariable=var, font=("Courier", 12)).grid(row=i//2, column=(i%2)*2+1, padx=10, pady=5, sticky='w')
            self.reg_vars[reg] = var

        self.tab_mem = ttk.Frame(notebook)
        notebook.add(self.tab_mem, text="Memory Dump")
        self.mem_addr_var = tk.StringVar(value="0000")
        addr_frame = ttk.Frame(self.tab_mem)
        addr_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(addr_frame, text="Dirección Hex:").pack(side=tk.LEFT)
        ttk.Entry(addr_frame, textvariable=self.mem_addr_var, width=6).pack(side=tk.LEFT, padx=5)
        ttk.Button(addr_frame, text="Ver", command=self.update_memory_dump).pack(side=tk.LEFT)
        self.mem_text = scrolledtext.ScrolledText(self.tab_mem, font=("Courier", 10), width=60, height=20)
        self.mem_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tab_repl = ttk.Frame(notebook)
        notebook.add(self.tab_repl, text="Interactive")
        self.repl_entry = ttk.Entry(self.tab_repl, font=("Courier", 12))
        self.repl_entry.pack(fill=tk.X, padx=5, pady=5)
        self.repl_entry.bind("<Return>", self.execute_repl)
        ttk.Label(self.tab_repl, text="Escribe comandos BASIC y pulsa ENTER.").pack()

        # Tab: Editor
        self.tab_editor = ttk.Frame(notebook)
        notebook.add(self.tab_editor, text="Editor")
        
        toolbar = ttk.Frame(self.tab_editor)
        toolbar.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(toolbar, text="▶ RUN", command=self.run_editor_code).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="⏹ STOP", command=self.stop_execution).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Limpiar", command=lambda: self.editor_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(toolbar, text=" Guardar como:").pack(side=tk.LEFT, padx=2)
        self.save_filename = tk.StringVar(value="MIPROG")
        ttk.Entry(toolbar, textvariable=self.save_filename, width=10).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="💾 SAVE (al DSK)", command=self.save_editor_code).pack(side=tk.LEFT, padx=5)
        
        self.editor_text = scrolledtext.ScrolledText(self.tab_editor, wrap=tk.WORD, font=("Courier", 12))
        self.editor_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.editor_text.bind("<KeyRelease>", self.highlight_syntax)
        self.setup_tags()
        
        default_code = '''10 MODE 1\n20 PAPER 0\n30 PEN 1\n40 LOCATE 10, 10\n50 PRINT "HOLA DESDE EL EDITOR!"\n60 FOR I=1 TO 5\n70 PEN I\n80 PRINT "COLOR ", I\n90 NEXT I\n'''
        self.editor_text.insert(tk.END, default_code)
        self.highlight_syntax()

    def update_speed(self):
        speed = self.speed_var.get()
        self.interpreter.speed = speed

    def new_file(self):
        self.editor_text.delete(1.0, tk.END)
        self.highlight_syntax()

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("BASIC Files", "*.bas *.cpcbas"), ("All Files", "*.*")])
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    code = f.read()
            except UnicodeDecodeError:
                with open(filepath, "r", encoding="latin-1") as f:
                    code = f.read()
            self.editor_text.delete(1.0, tk.END)
            self.editor_text.insert(tk.END, code)
            self.highlight_syntax()
            
    def save_as_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".bas", filetypes=[("BASIC Files", "*.bas *.cpcbas"), ("All Files", "*.*")])
        if filepath:
            code = self.editor_text.get(1.0, tk.END)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)

    def show_colors(self):
        win = tk.Toplevel(self.root)
        win.title("Paleta de Colores CPC")
        win.geometry("400x400")
        text = scrolledtext.ScrolledText(win, font=("Courier", 10))
        text.pack(fill=tk.BOTH, expand=True)
        colors = """Colores Hardware Amstrad CPC:

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
"""
        text.insert(tk.END, colors)
        text.config(state=tk.DISABLED)

    def show_ascii(self):
        win = tk.Toplevel(self.root)
        win.title("Tabla ASCII")
        win.geometry("300x500")
        text = scrolledtext.ScrolledText(win, font=("Courier", 10))
        text.pack(fill=tk.BOTH, expand=True)
        ascii_table = """Tabla de caracteres (selección):
  
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
   33 !    34 "    35 #
   36 $    37 %    38 &
   39 '    40 (    41 )
   42 *    43 +    44 ,
   45 -    46 .    47 /
   48 0 .. 57 9
"""
        text.insert(tk.END, ascii_table)
        text.config(state=tk.DISABLED)

    def show_coords(self):
        win = tk.Toplevel(self.root)
        win.title("Guía de Coordenadas Gráficas")
        win.geometry("500x350")
        text = scrolledtext.ScrolledText(win, font=("Courier", 10))
        text.pack(fill=tk.BOTH, expand=True)
        coords = """Sistema de Coordenadas Gráficas (CPC):
  
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
"""
        text.insert(tk.END, coords)
        text.config(state=tk.DISABLED)

    def setup_tags(self):
        self.editor_text.tag_configure("keyword", foreground="blue")
        self.editor_text.tag_configure("string", foreground="green")
        self.editor_text.tag_configure("comment", foreground="gray")
        self.editor_text.tag_configure("number", foreground="darkorange")

    def highlight_syntax(self, event=None):
        import re
        for tag in ["keyword", "string", "comment", "number"]:
            self.editor_text.tag_remove(tag, "1.0", tk.END)
            
        content = self.editor_text.get("1.0", tk.END)
        
        keywords = ["PRINT", "LOCATE", "MODE", "PAPER", "PEN", "FOR", "TO", "STEP", "NEXT", "IF", "THEN", "ELSE", "GOTO", "GOSUB", "RETURN", "DIM", "DATA", "READ", "RESTORE", "INK", "BORDER", "PLOT", "DRAW", "DRAWR", "MOVE", "MOVER", "DEFINT", "DEFREAL", "DEFSTR", "CALL", "ENV", "ENT", "SOUND", "ON", "STOP", "END", "CLS", "CLG", "WINDOW", "INPUT", "WHILE", "WEND", "FILL", "MASK", "GRAPHICS", "TAG", "TAGOFF", "ORIGIN", "DI", "EI", "REM", "CLEAR", "SYMBOL", "ABS", "ASC", "CHR\$", "CINT", "COS", "CREAL", "EXP", "FIX", "INT", "LEFT\$", "LEN", "LOG", "LOG10", "LOWER\$", "MID\$", "PI", "POS", "RIGHT\$", "RND", "SGN", "SIN", "SPACE\$", "SQ", "SQR", "STR\$", "STRING\$", "TAN", "TEST", "TESTR", "TIME", "UNT", "UPPER\$", "VAL", "VPOS", "XPOS", "YPOS", "INKEY", "INKEY\$", "JOY", "PEEK", "ROUND", "PAUSE"]
        kw_pattern = r"\b(" + "|".join(keywords) + r")\b"
        
        patterns = {
            "string": r'".*?"',
            "comment": r"('.*|\bREM\b.*)",
            "keyword": kw_pattern,
            "number": r"\b\d+\b"
        }
        
        for tag, pattern in patterns.items():
            for match in re.finditer(pattern, content, re.IGNORECASE):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.editor_text.tag_add(tag, start, end)

    def load_dsk(self):
        filepath = filedialog.askopenfilename(filetypes=[("DSK Images", "*.dsk")])
        if filepath:
            if self.dsk:
                self.dsk.unmount()
            self.dsk = DSKManager(filepath)
            if self.dsk.mount():
                self.interpreter.dsk = self.dsk
                files = self.dsk.list_files()
                bas_files = [f for f in files if f.lower().endswith(".bas") or f.lower().endswith(".cpcbas")]
                if bas_files:
                    code = self.dsk.read_file(bas_files[0])
                    self.repl_queue.put(('RUN', code))
                else:
                    tk.messagebox.showinfo("DSK", f"Catálogo:\n{chr(10).join(files)}\nNo se encontró .BAS")
            else:
                tk.messagebox.showerror("Error", "No se pudo montar el disco.")

    def save_editor_code(self):
        if not self.dsk or not self.dsk.mounted:
            tk.messagebox.showerror("Error", "No hay ningún disco DSK montado. Carga uno primero desde Archivo -> Cargar DSK.")
            return
            
        filename = self.save_filename.get().strip().upper()
        if not filename:
            filename = "MIPROG.BAS"
        if not filename.endswith(".BAS"):
            filename += ".BAS"
            
        code = self.editor_text.get(1.0, tk.END)
        if self.dsk.write_file(filename, code):
            tk.messagebox.showinfo("Éxito", f"Programa guardado como {filename} en el disco virtual.")
        else:
            tk.messagebox.showerror("Error", f"Fallo al guardar {filename}.")

    def run_editor_code(self):
        code = self.editor_text.get(1.0, tk.END)
        self.repl_queue.put(('RUN', code))

    def stop_execution(self):
        print("[UI] STOP button clicked")
        self.interpreter.running = False
        if hasattr(self.interpreter, 'display'):
            self.interpreter.display.quit_requested = True
            import pygame
            if pygame.display.get_surface() is not None:
                self.interpreter.display.print_text("Break\r\n")
                self.interpreter.display.update()
            
        # Limpiar cualquier cola pendiente
        while not self.repl_queue.empty():
            try:
                self.repl_queue.get_nowait()
            except queue.Empty:
                break
                
        # Reiniciar variables para evitar cuelgues al hacer run de nuevo
        self.interpreter.pc = None
        self.interpreter.current_line_idx = 0
        if hasattr(self.interpreter, 'display'):
            self.interpreter.display.clear_input()

    def execute_repl(self, event):
        cmd = self.repl_entry.get()
        self.repl_entry.delete(0, tk.END)
        
        import re
        m_load = re.match(r'^\s*LOAD\s+"([^"]+)"', cmd, re.IGNORECASE)
        if m_load:
            filename = m_load.group(1)
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    code = f.read()
                self.editor_text.delete('1.0', tk.END)
                self.editor_text.insert(tk.END, code)
                print(f"[IDE] Archivo '{filename}' cargado en el editor.")
                # We load it into memory but do not execute it automatically
                self.repl_queue.put(('LOAD_ONLY', code))
            except Exception as e:
                print(f"[IDE] Error cargando '{filename}': {e}")
            return
            
        m_save = re.match(r'^\s*SAVE\s+"([^"]+)"', cmd, re.IGNORECASE)
        if m_save:
            filename = m_save.group(1)
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.editor_text.get('1.0', tk.END).strip() + '\n')
                print(f"[IDE] Archivo '{filename}' guardado desde el editor.")
            except Exception as e:
                print(f"[IDE] Error guardando '{filename}': {e}")
            return

        self.repl_queue.put(('CMD', cmd))

    def update_memory_dump(self):
        try:
            addr = int(self.mem_addr_var.get(), 16)
        except ValueError:
            addr = 0
        mem = self.interpreter.bank_memory
        lines = []
        for i in range(0, 256, 16):
            if addr + i >= 65536: break
            chunk = mem[addr + i : addr + i + 16]
            hex_str = " ".join([f"{b:02X}" for b in chunk])
            ascii_str = "".join([chr(b) if 32 <= b <= 126 else "." for b in chunk])
            lines.append(f"{addr + i:04X}  {hex_str:<48}  {ascii_str}")
        self.mem_text.delete(1.0, tk.END)
        self.mem_text.insert(tk.END, "\n".join(lines))

    def emulator_thread_loop(self):
        # We need a dummy program just to keep Pygame display alive when idle
        class DummyProgram:
            def __init__(self):
                self.lines = {}
        self.interpreter.program = DummyProgram()
        
        while True:
            try:
                task = self.repl_queue.get(timeout=0.05)
                cmd_type, data = task
                if cmd_type == 'RUN':
                    lexer = Lexer(data)
                    parser = Parser(lexer.tokens)
                    self.interpreter.program = parser.parse()
                    self.interpreter.reset()
                    self.interpreter.line_numbers = sorted(list(self.interpreter.program.lines.keys()))
                    print("[THREAD] Calling execute()...")
                    self.interpreter.execute()
                    print("[THREAD] execute() returned.")
                elif cmd_type == 'LOAD_ONLY':
                    lexer = Lexer(data)
                    parser = Parser(lexer.tokens)
                    self.interpreter.program = parser.parse()
                    self.interpreter.line_numbers = sorted(list(self.interpreter.program.lines.keys()))
                    print("[THREAD] Program loaded into memory.")
                elif cmd_type == 'CMD':
                    lexer = Lexer(data)
                    parser = Parser(lexer.tokens)
                    stmt = parser.parse_statement()
                    if stmt:
                        class TmpProgram:
                            def __init__(self, s):
                                self.lines = {-1: [s]}
                        self.interpreter.program = TmpProgram(stmt)
                        self.interpreter.line_numbers = [-1]
                        print("[THREAD] Calling execute()...")
                    self.interpreter.execute()
                    print("[THREAD] execute() returned.")
            except queue.Empty:
                # Keep Pygame responsive
                if hasattr(self.interpreter, 'display'):
                    self.interpreter.display.process_events()
                    self.interpreter.display.update()
                    pygame.time.wait(20)
            except Exception as e:
                print(f"Emulator error: {e}")

    def update_gui(self):
        z80 = self.interpreter.z80
        self.reg_vars['A'].set(f"{z80.A:02X}")
        self.reg_vars['F'].set(f"{z80.F:02X}")
        self.reg_vars['B'].set(f"{z80.B:02X}")
        self.reg_vars['C'].set(f"{z80.C:02X}")
        self.reg_vars['D'].set(f"{z80.D:02X}")
        self.reg_vars['E'].set(f"{z80.E:02X}")
        self.reg_vars['H'].set(f"{z80.H:02X}")
        self.reg_vars['L'].set(f"{z80.L:02X}")
        self.reg_vars['PC'].set(f"{z80.PC:04X}")
        self.reg_vars['SP'].set(f"{z80.SP:04X}")
        self.root.after(50, self.update_gui)

    def quit(self):
        if self.dsk:
            self.dsk.unmount()
        pygame.quit()
        self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = EmulatorGUI(root)
    root.mainloop()
