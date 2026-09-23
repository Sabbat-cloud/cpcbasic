import sys
import os

# Forzar driver de audio DirectSound para evitar crashes con monitores HDMI
if sys.platform == 'win32':
    os.environ['SDL_AUDIODRIVER'] = 'directsound'

import pygame
# Configurar mezclador a 44100Hz (frecuencia clásica/original)
pygame.mixer.pre_init(44100, -16, 2, 1024)

import argparse
from core.lexer import Lexer
from core.parser import Parser
from core.interpreter import Interpreter

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Amstrad CPC BASIC Emulator")
    parser.add_argument("filename", nargs="?", help="Archivo .cpcbas a ejecutar")
    parser.add_argument("--scale", type=int, default=2, help="Escalado de la ventana (ej. 2, 3)")
    parser.add_argument("--list", action="store_true", help="Solo muestra el listado del código y sale, sin ejecutarlo")
    args = parser.parse_args()

    if args.filename:
        if args.filename.lower().endswith('.dsk'):
            from core.storage import DSKManager
            print(f"--- Montando DSK {args.filename} ---")
            dsk = DSKManager(args.filename)
            if dsk.mount():
                files = dsk.list_files()
                print("Catálogo del disco:")
                for f in files:
                    print(f"  {f}")
                    
                bas_files = [f for f in files if f.lower().endswith(".bas") or f.lower().endswith(".cpcbas")]
                if bas_files:
                    run_file = bas_files[0]
                    print(f"--- Auto-Cargando {run_file} ---")
                    code = dsk.read_file(run_file)
                    dsk.unmount()
                else:
                    print("No se encontró ningún archivo BASIC (.BAS) para ejecutar.")
                    dsk.unmount()
                    sys.exit(0)
            else:
                sys.exit(1)
        else:
            print(f"--- Loading {args.filename} ---")
            try:
                with open(args.filename, "r", encoding="utf-8") as f:
                    code = f.read()
            except FileNotFoundError:
                print(f"Error: No se encontró el archivo {args.filename}")
                sys.exit(1)
    else:
        # Default code if no file provided
        code = """
10 MODE 1
20 PAPER 0
30 PEN 1
40 LOCATE 15, 1
50 PRINT "--- AMSTRAD CPC ---"
60 FOR I=1 TO 5
70 PEN I
80 LOCATE 5, 5 + I
90 PRINT "COLOR LOOP"
100 NEXT I
110 SOUND 1, 142, 50, 15
"""
        print("--- Usando código por defecto (pasa un fichero .cpcbas como argumento) ---")

    if args.list:
        print("\n--- LISTADO DEL CÓDIGO ---")
        print(code)
        sys.exit(0)

    print("--- Tokens ---")
    lexer = Lexer(code)
        
    print("\n--- Parsing ---")
    parser = Parser(lexer.tokens)
    program = parser.parse()
    
    print("\n--- Execution ---")
    interpreter = Interpreter(program, scale=args.scale)
    
    interpreter.execute()
