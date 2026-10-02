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
        file_menu.add_command(label="Cargar DSK...", command=self.load_dsk)
        file_menu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)
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
        
        default_code = '''10 MODE 1\n20 PAPER 0\n30 PEN 1\n40 LOCATE 10, 10\n50 PRINT "HOLA DESDE EL EDITOR!"\n60 FOR I=1 TO 5\n70 PEN I\n80 PRINT "COLOR ", I\n90 NEXT I\n'''
        self.editor_text.insert(tk.END, default_code)

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
