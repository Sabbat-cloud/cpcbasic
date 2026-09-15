import os
import sys
import subprocess
import tempfile
import shutil

class DSKManager:
    """
    Gestor de imágenes de disco Amstrad CPC (.dsk)
    Utiliza el motor de muckypaws/AmstradDSKExplorer
    """
    def __init__(self, filename):
        self.filename = filename
        self.dsk_tool = os.path.join("assets", "AmstradDSKExplorer-master", "DSKInfoV3.py")
        self.mounted = False
        self.temp_dir = None
        
    def mount(self):
        """Monta el disco y extrae los archivos a un directorio temporal"""
        if not os.path.exists(self.filename):
            print(f"Error: No se encontró el disco {self.filename}")
            return False
            
        if not os.path.exists(self.dsk_tool):
            print("Error: AmstradDSKExplorer no está instalado en assets/")
            return False
            
        print(f"[DSK] Montando disco {self.filename}...")
        self.temp_dir = tempfile.mkdtemp(prefix="cpcbasic_dsk_")
        
        try:
            # Ejecutamos la herramienta para extraer todo (-dir -ex) en la misma carpeta
            # porque la herramienta extrae los ficheros en el CWD donde se ejecuta.
            # Por tanto, cambiamos el CWD temporalmente.
            dsk_abspath = os.path.abspath(self.filename)
            tool_abspath = os.path.abspath(self.dsk_tool)
            
            subprocess.run(
                [sys.executable, tool_abspath, "-dir", "-ex", dsk_abspath],
                cwd=self.temp_dir,
                capture_output=True,
                text=True
            )
            self.mounted = True
            return True
        except Exception as e:
            print(f"Error extrayendo DSK: {e}")
            return False
            
    def unmount(self):
        """Limpia el directorio temporal"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        self.mounted = False
        
    def list_files(self):
        """Devuelve la lista de archivos extraídos"""
        if not self.mounted:
            return []
        return os.listdir(self.temp_dir)
        
    def read_file(self, filename):
        """
        Lee el contenido de un archivo extraído.
        Se asume que fue guardado en ASCII (SAVE "FILE", A).
        """
        if not self.mounted:
            return None
            
        # DSKInfoV3 extrae manteniendo los nombres en mayúsculas típicamente
        target_path = os.path.join(self.temp_dir, filename.upper())
        if not os.path.exists(target_path):
            target_path = os.path.join(self.temp_dir, filename)
            
        if os.path.exists(target_path):
            try:
                # Quitamos la cabecera AMSDOS de 128 bytes si DSKInfoV3 no lo hizo
                # DSKInfoV3 guarda el binario completo con la cabecera
                with open(target_path, "rb") as f:
                    data = f.read()
                    
                if len(data) > 128:
                    # Las cabeceras de Amstrad tienen checksums y user info
                    # Si el archivo era de texto, a partir del byte 128 suele estar el ASCII plano
                    # Vamos a intentar leerlo como texto a partir del byte 128
                    text_data = data[128:].decode('utf-8', errors='ignore')
                    # Limpiamos ceros binarios del final (padding del sector)
                    text_data = text_data.strip('\x00\x1a')
                    return text_data
            except Exception as e:
                print(f"Error leyendo {filename}: {e}")
                
        return None
