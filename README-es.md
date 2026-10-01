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
- **Arquitectura de Emulación Híbrida (Memoria y Z80)**: Implementa una matriz de RAM virtual de 64KB con sincronización bidireccional de vídeo. Los comandos `PEEK` y `POKE` sobre la memoria del CRTC (`&C000` a `&FFFF`) interactúan dinámicamente con los píxeles de PyGame, replicando la estructura del hardware original. Además, dispone de un "Z80 Fantasma" (registros `_REG_A`, `_REG_HL`, etc.) que te permite alterar directamente el estado del procesador desde el propio código BASIC antes de lanzar un comando `CALL` al firmware.
- **Soporte de Lectura de Discos (.dsk)**: Montaje "al vuelo" de archivos `.dsk`. Extrae y ejecuta de forma transparente archivos BASIC en texto plano (ASCII) almacenados dentro de formatos AMSDOS.
- **Ejecución Optimizada y Control de Velocidad**: Generación y caché de código AST en segundo plano, consiguiendo velocidades ultrarrápidas en modo de ejecución sin límites. Adicionalmente ofrece un límite opcional que reproduce la velocidad exacta de ejecución del procesador original del Amstrad CPC 6128.

*(Nota: No soporta archivos BASIC binarios tokenizados ni binarios nativos de código máquina Z80 compilados, dado que es un intérprete de alto nivel, no un emulador puro de hardware. Sin embargo, gracias al Z80 fantasma, intercepta llamadas de firmware nativas de Amstrad ROM y emula su respuesta directamente en Python).*

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

Puedes ejecutar el emulador pasándole un script BASIC como argumento. Por defecto, la ventana se escala al doble (x2), pero puedes cambiarlo con `--scale`. También puedes controlar la velocidad de ejecución con el parámetro `--speed` (utiliza `real` para simular el hardware original o `unlimited` para máxima velocidad).

```bash
python main.py examples/matrix.cpcbas --scale 3 --speed real
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
- **`tecnicasproggraficos/`**: Dentro de `examples/` tenéis multitud de ejemplos, incluido el listado completo con todos los ejemplos del libro *"Técnicas de programación gráfica"* en `examples/tecnicasproggraficos/`.
- **Ejemplos del Manual Oficial**: Gracias a las últimas actualizaciones en variables de cadena y matemáticas, la mayoría de los ejemplos sencillos del *Manual de Usuario de Locomotive BASIC* pueden probarse directamente (por ejemplo, pegándolos en `temp_run.cpcbas`) y funcionarán a la primera.

## ¿Por qué?
La respuesta corta es por diversión. Crecí con el BASIC del Amstrad CPC y a veces me apetecía probar pequeñas cosas, ya sea por nostalgia o curiosidad, y poder acceder al BASIC sin tener que cargar todo el entorno del emulador me parecía práctico.
Se pueden editar los listados con el programa que quieras sin tener que depender del emulador, montar unidades de disco, etc.
Actualmente ya está soportado el acceso aleatorio a ficheros, con lo que podemos escribir, leer y modificar cualquier fichero de nuestro PC para procesarlo con nuestros programas en BASIC.
Por supuesto, también está la ausencia de limitación de memoria y el aumento de la velocidad.
Su carencia más obvia es la falta de ejecución completa y pura de código máquina. Sin embargo, gracias a la nueva Arquitectura Híbrida, las llamadas estándar al firmware (como `CALL &BB5A`, `CALL &BB18`) son interceptadas. ¡Puedes manipular los registros virtuales del procesador Z80 directamente desde BASIC usando variables especiales (ej. `_REG_A = 65`) antes de llamar al firmware, y el motor en Python simulará la respuesta del hardware al instante leyendo tus registros y ejecutando la rutina!


## Créditos y Agradecimientos
- Tipografía: [damianvila/font-cpc464](https://github.com/damianvila/font-cpc464)
- Lógica de Discos inspirada por: [muckypaws/AmstradDSKExplorer](https://github.com/muckypaws/AmstradDSKExplorer)

## Licencia
Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE](LICENSE) para más detalles.
