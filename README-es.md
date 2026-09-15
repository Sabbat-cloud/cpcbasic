# Emulador CPCBasic

*[Read this in English](README.md)*

CPCBasic es un intérprete de alto nivel de Locomotive BASIC de Amstrad CPC escrito completamente en Python. En lugar de emular la arquitectura del hardware Z80 ciclo a ciclo, este emulador implementa un analizador (Parser) AST (Abstract Syntax Tree) personalizado que lee archivos de texto plano en BASIC (`.cpcbas` o `.bas` en ASCII) y los ejecuta directamente utilizando software moderno.

Utiliza `pygame` para una reproducción audiovisual de gran fidelidad, capturando por completo la esencia estética de la máquina de 8 bits clásica.

## Características

- **Tokenizador Léxico y Parser AST**: Interpretación completa de palabras clave de Locomotive BASIC, bucles lógicos (`FOR`, `IF/THEN`), subrutinas (`GOSUB`/`RETURN`) y funciones matemáticas.
- **Subsistema Gráfico Auténtico**: Utiliza la paleta de colores del Amstrad CPC y soporta las resoluciones de hardware estándar (`MODE 0`, `MODE 1`, `MODE 2`) con escalado de píxeles adecuado.
- **Fuente de Píxeles Original**: Integra la fuente de píxeles original del CPC464 para una experiencia de renderizado de texto 1:1 (`LOCATE`, `PRINT`, `PEN`, `PAPER`).
- **Audio Procedural (AY-3-8912)**: Interpreta de manera precisa el comando `SOUND` y genera ondas cuadradas y ruido blanco procedurales en tiempo real mediante `numpy` y el mixer de Pygame.
- **Interacción con el Teclado**: Soporte para lectura asíncrona de teclado (`INKEY$`).
- **Soporte de Lectura de Discos (.dsk)**: Montaje "al vuelo" de archivos `.dsk`. Extrae y ejecuta de forma transparente archivos BASIC en texto plano (ASCII) almacenados dentro de formatos AMSDOS.

*(Nota: No soporta archivos BASIC binarios tokenizados ni binarios de código máquina Z80 compilados, dado que es un intérprete de lenguaje de alto nivel, no un emulador de CPU).*

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

También puedes ejecutar imágenes `.dsk` directamente, siempre y cuando los scripts en su interior estén guardados en formato ASCII:
```bash
python main.py midisco.dsk
```

## Ejemplos

Revisa la carpeta `examples/` para probar las capacidades:
- `matrix.cpcbas`: Una demo visual de colores, números aleatorios, bucles y sonido procedural.
- `teclado.cpcbas`: Un bucle de interacción de teclado en tiempo real usando `INKEY$`.
- `hola.cpcbas`: Un simple "Hola Mundo" demostrando el dibujado de líneas y cambio de tintas.

## Créditos y Agradecimientos
- Tipografía: [damianvila/font-cpc464](https://github.com/damianvila/font-cpc464)
- Lógica de Discos inspirada por: [muckypaws/AmstradDSKExplorer](https://github.com/muckypaws/AmstradDSKExplorer)
