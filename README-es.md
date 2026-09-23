# Emulador CPCBasic

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Amstrad CPC](https://img.shields.io/badge/Plataforma-Amstrad_CPC-red.svg)
![Locomotive BASIC](https://img.shields.io/badge/Lenguaje-Locomotive_BASIC-yellow.svg)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green.svg)
*[Read this in English](README.md)*

CPCBasic es un intérprete de alto nivel de Locomotive BASIC de Amstrad CPC escrito completamente en Python. En lugar de emular la arquitectura del hardware Z80 ciclo a ciclo, este emulador implementa un analizador (Parser) AST (Abstract Syntax Tree) personalizado que lee archivos de texto plano en BASIC (`.cpcbas` o `.bas` en ASCII) y los ejecuta directamente utilizando software moderno.

Utiliza `pygame` para una reproducción audiovisual de gran fidelidad, capturando por completo la esencia estética de la máquina de 8 bits clásica.

## Características

- **Tokenizador Léxico y Parser AST**: Interpretación completa de palabras clave de Locomotive BASIC. El módulo `core/parser.py` implementa un analizador descendente recursivo (Recursive Descent Parser) que convierte la secuencia de tokens en un Árbol de Sintaxis Abstracta (AST). Maneja de forma robusta la sintaxis compleja de Amstrad: múltiples sentencias por línea separadas por dos puntos (`:`), bucles anidados, condiciones `IF/THEN/ELSE`, operaciones matemáticas complejas, expresiones y sentencias exclusivas del sistema como las relativas a interrupciones y memoria.
- **Funciones Matemáticas y de Cadena**: 100% de cobertura matemática del estándar Amstrad (`ATN`, `SIN`, `COS`, `TAN`, `PI`, `SQR`, `INT`, `FIX`, `ROUND`, `CINT`, `CREAL`, `UNT`, `LOG`, `MAX`, `MIN`, `EXP`, `SGN`) y amplio soporte de cadenas (`CHR$`, `COPYCHR$`, `LEFT$`, `UPPER$`, `STR$`, `SPACE$`, `STRING$`, `HEX$`, `BIN$`, `INSTR`, `DEC$`).
- **Control Avanzado de Terminal**: Soporte completo para los caracteres de control mediante `CHR$()`, permitiendo saltos de línea, movimientos del cursor (`CHR$(11)`), transparencia y sobreimpresión de texto (`CHR$(22)`), y video inverso/intercambio de tintas (`CHR$(24)`).
- **Subsistema Gráfico Auténtico**: Utiliza la paleta de colores de firmware estándar del Amstrad CPC y soporta resoluciones de hardware (`MODE 0`, `MODE 1`, `MODE 2`). Implementa comandos gráficos como `PLOT`, `DRAW`, `MOVE`, `ORIGIN`, y `CLG`.
- **Cadenas y Salida de Terminal**: Maneja correctamente las instrucciones `PRINT` con separadores (`,`, `;`), además de soporte para streams (`#`).
- **Fuente de Píxeles Original**: Integra la fuente de píxeles original del CPC464 para una experiencia de renderizado de texto 1:1 (`LOCATE`, `PRINT`, `PEN`, `PAPER`).
- **Audio Procedural (AY-3-8912)**: Interpreta de manera precisa el comando `SOUND` y genera ondas cuadradas y ruido blanco procedurales en tiempo real mediante `numpy` y el mixer de Pygame.
- **Interacción con Teclado y Joysticks**: Soporte para lectura asíncrona de teclado (`INKEY$`, `INKEY`), pausas de hardware (`CALL &BB18`, `PAUSE 0`) y joysticks simulados mediante Pygame (`JOY`).
- **Memoria Virtual (PEEK/POKE)**: Implementa una matriz de RAM virtual de 64KB y llamadas a memoria simuladas (`CALL`), lo que permite que scripts antiguos se ejecuten sin lanzar errores por falta de memoria.
- **Soporte de Lectura de Discos (.dsk)**: Montaje "al vuelo" de archivos `.dsk`. Extrae y ejecuta de forma transparente archivos BASIC en texto plano (ASCII) almacenados dentro de formatos AMSDOS.

*(Nota: No soporta archivos BASIC binarios tokenizados ni binarios de código máquina Z80 compilados, dado que es un intérprete de lenguaje de alto nivel, no un emulador de CPU).*

**⚠️ ADVERTENCIA: Este emulador se encuentra en una etapa temprana de desarrollo. Muchas características podrían fallar.**

## Instalación

1. Clona este repositorio.
2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Puedes ejecutar el emulador pasándole un script basic como argumento. Por defecto, la ventana se escala al doble (x2), pero puedes cambiarlo con `--scale`.

```bash
python main.py examples/matrix.cpcbas --scale 3
```

También puedes ejecutar imágenes `.dsk` directamente:
```bash
python main.py midisco.dsk
```

## Ejemplos Completos

Revisa la carpeta `examples/` para probar las capacidades del emulador. Algunos de los más de 20 ejemplos incluidos son:
- **`matrix.cpcbas`**: Efecto Matrix que demuestra el uso de colores, números aleatorios, bucles y sonido procedural.
- **`juego_reflejos.cpcbas`**: Un juego completo con temporizadores asíncronos (`AFTER`/`EVERY`), envolventes de volumen/tono, lectura física del teclado (`INKEY`) y manejo complejo de pantalla.
- **`demo_colores.cpcbas`**: Intercambio de colores de bordes y tintas usando temporizadores lógicos.
- **`subrrayadotexto.cpcbas` y `videoinverso.cpcbas`**: Ejemplos del uso de caracteres de control avanzados como la transparencia (`CHR$(22)`) y el video inverso (`CHR$(24)`).
- **`pause.cpcbas`**: Demostración de las pausas del sistema mediante `CALL &BB18` y `PAUSE 0`.
- **`movimiento.cpcbas` y `teclado.cpcbas`**: Demos gráficas interactuando con el búfer de teclado en tiempo real.
- **`sprite.cpcbas`**: Creación de gráficos definidos por el usuario con `SYMBOL`.
- **`circulos.cpcbas`, `figura3.cpcbas`, `cuadrados.cpcbas`**: Extensas pruebas gráficas de dibujo (`PLOT`, `DRAW`, matemáticas trigonométricas).

- **Ejemplos del Manual Oficial**: Gracias a las últimas actualizaciones en variables de cadena y matemáticas, la mayoría de los ejemplos sencillos del *Manual de Usuario de Locomotive BASIC* pueden probarse directamente (por ejemplo, pegándolos en 	emp_run.cpcbas) y funcionarán a la primera.

## Créditos y Agradecimientos
- Tipografía: [damianvila/font-cpc464](https://github.com/damianvila/font-cpc464)
- Lógica de Discos inspirada por: [muckypaws/AmstradDSKExplorer](https://github.com/muckypaws/AmstradDSKExplorer)

## Licencia
Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE](LICENSE) para más detalles.
