# Emulador CPCBasic

*[Read this in English](README.md)*

CPCBasic es un intérprete de alto nivel de Locomotive BASIC de Amstrad CPC escrito completamente en Python. En lugar de emular la arquitectura del hardware Z80 ciclo a ciclo, este emulador implementa un analizador (Parser) AST (Abstract Syntax Tree) personalizado que lee archivos de texto plano en BASIC (`.cpcbas` o `.bas` en ASCII) y los ejecuta directamente utilizando software moderno.

Utiliza `pygame` para una reproducción audiovisual de gran fidelidad, capturando por completo la esencia estética de la máquina de 8 bits clásica.

## Características

- **Tokenizador Léxico y Parser AST**: Interpretación completa de palabras clave de Locomotive BASIC, bucles lógicos (`FOR`, `IF/THEN`), subrutinas (`GOSUB`/`RETURN`) y funciones matemáticas.
- **Subsistema Gráfico Auténtico**: Utiliza la paleta de colores de firmware estándar del Amstrad CPC y soporta resoluciones de hardware (`MODE 0`, `MODE 1`, `MODE 2`). Implementa comandos gráficos como `PLOT`, `DRAW`, `MOVE`, `ORIGIN`, y `CLG`.
- **Cadenas y Salida de Terminal**: Maneja correctamente las instrucciones `PRINT` con separadores (`,`, `;`), además de funciones de cadena como `CHR$`.
- **Fuente de Píxeles Original**: Integra la fuente de píxeles original del CPC464 para una experiencia de renderizado de texto 1:1 (`LOCATE`, `PRINT`, `PEN`, `PAPER`).
- **Audio Procedural (AY-3-8912)**: Interpreta de manera precisa el comando `SOUND` y genera ondas cuadradas y ruido blanco procedurales en tiempo real mediante `numpy` y el mixer de Pygame.
- **Interacción con el Teclado**: Soporte para lectura asíncrona de teclado (`INKEY$`).
- **Soporte de Lectura de Discos (.dsk)**: Montaje "al vuelo" de archivos `.dsk`. Extrae y ejecuta de forma transparente archivos BASIC en texto plano (ASCII) almacenados dentro de formatos AMSDOS.

*(Nota: No soporta archivos BASIC binarios tokenizados ni binarios de código máquina Z80 compilados, dado que es un intérprete de lenguaje de alto nivel, no un emulador de CPU).*

**⚠️ ADVERTENCIA: Este emulador se encuentra en una etapa muy temprana de desarrollo (estado inicial). Muchas características, instrucciones o comportamientos todavía no están implementados, y muchas cosas podrían fallar.**

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

Revisa la carpeta `examples/` para probar las capacidades del emulador:
- `matrix.cpcbas`: Efecto Matrix que demuestra el uso de colores, números aleatorios, bucles y sonido procedural.
- `juego_reflejos.cpcbas`: Un juego completo con temporizadores asíncronos (`AFTER`/`EVERY`), envolventes de volumen/tono, lectura física del teclado (`INKEY`) y manejo complejo de pantalla.
- `demo_colores.cpcbas`: Intercambio de colores de bordes y tintas usando temporizadores lógicos.
- `movimiento.cpcbas`: Demo gráfica moviendo elementos interactivos.
- `teclado.cpcbas`: Un bucle de interacción de teclado en tiempo real usando el búfer `INKEY$`.
- `circulos.cpcbas` y similares: Pruebas gráficas de dibujo (`PLOT`, `DRAW`, matemáticas trigonométricas).

## Créditos y Agradecimientos
- Tipografía: [damianvila/font-cpc464](https://github.com/damianvila/font-cpc464)
- Lógica de Discos inspirada por: [muckypaws/AmstradDSKExplorer](https://github.com/muckypaws/AmstradDSKExplorer)

## Licencia
Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE](LICENSE) para más detalles.
