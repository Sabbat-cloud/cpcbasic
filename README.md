# CPCBasic Emulator

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Amstrad CPC](https://img.shields.io/badge/Platform-Amstrad_CPC-red.svg)
![Locomotive BASIC](https://img.shields.io/badge/Language-Locomotive_BASIC-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
*[Read this in Spanish (Leer en Español)](README-es.md)*

CPCBasic is a high-level Amstrad CPC Locomotive BASIC interpreter written entirely in Python. Instead of emulating the Z80 hardware architecture cycle by cycle, this emulator implements a custom AST (Abstract Syntax Tree) Parser that reads pure BASIC plain-text files (`.cpcbas` or ASCII `.bas`) and executes them directly using modern software.

It uses `pygame` for highly accurate audiovisual reproduction, capturing the aesthetic feel of the classic 8-bit machine.

## Features

- **Lexical Tokenizer & AST Parser**: Full interpretation of Locomotive BASIC keywords. The `core/parser.py` module implements a Recursive Descent Parser that converts the token sequence into an Abstract Syntax Tree (AST). It robustly handles Amstrad's complex syntax: multiple statements per line separated by colons (`:`), nested loops, `IF/THEN/ELSE` conditions, complex mathematical operations, and system-exclusive expressions like interrupts and memory management.
- **Math & String Functions**: 100% complete standard Amstrad mathematics (ATN, SIN, COS, TAN, PI, SQR, INT, FIX, ROUND, CINT, CREAL, UNT, LOG, MAX, MIN, EXP, SGN) and string manipulations (CHR$, COPYCHR$, LEFT$, UPPER$, STR$, SPACE$, STRING$, HEX$, BIN$, INSTR, DEC$).
- **Advanced Terminal Control**: Full support for control characters via `CHR$()`, enabling line feeds, cursor movements (`CHR$(11)`), transparency and text overprinting (`CHR$(22)`), and inverse video/ink swapping (`CHR$(24)`).
- **Authentic Graphics Subsystem**: Uses the standard Amstrad CPC firmware colors. Supports standard hardware resolutions (MODE 0, MODE 1, MODE 2) with proper pixel scaling. It implements graphical commands such as PLOT, DRAW, MOVE, ORIGIN, and CLG.
- **String & Terminal Output**: Handles standard PRINT statements with separators (,, ;), along with stream support (`#`).
- **Original Pixel Font**: Integrates the original CPC464 pixel font for a 1:1 text rendering experience (LOCATE, PRINT, PEN, PAPER).
- **Procedural Audio (AY-3-8912)**: Accurately parses the SOUND command and generates procedural square waves and white noise in real-time via numpy and Pygame's mixer.
- **Keyboard & Joystick Interaction**: Support for asynchronous keyboard reading (INKEY$, INKEY), hardware pauses (`CALL &BB18`, `PAUSE 0`) and simulated Amstrad Joysticks using Pygame (JOY).
- **Virtual Memory (PEEK/POKE)**: Implements a 64KB virtual RAM array and simulated memory calls (`CALL`) allowing legacy scripts to execute successfully without crashing.
- **Disk (.dsk) Read Support**: On-the-fly mounting of .dsk files. It extracts and executes plain-text (ASCII) BASIC files stored within AMSDOS formats seamlessly.

*(Note: It does not support tokenized binary BASIC files or compiled Z80 machine code binaries since it is a high-level language interpreter, not a CPU emulator).*

**⚠️ WARNING: This emulator is in an early stage of development. Many features might fail or crash!**

## Installation

1. Clone this repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

You can run the emulator by passing a basic script as an argument. The window is scaled x2 by default, but you can change it with `--scale`.

```bash
python main.py examples/matrix.cpcbas --scale 3
```

You can also run `.dsk` images directly:
```bash
python main.py mydisk.dsk
```

## Complete Examples

Check the `examples/` folder to test the capabilities of the emulator. Some of the over 20 included examples are:
- **`matrix.cpcbas`**: A Matrix effect showcasing colors, random numbers, loops, and procedural sound.
- **`juego_reflejos.cpcbas`**: A complete reflex game using asynchronous timers (`AFTER`/`EVERY`), volume/tone envelopes, direct hardware keyboard reading (`INKEY`), and complex screen handling.
- **`demo_colores.cpcbas`**: A border and ink color cycling demo using software delays.
- **`subrrayadotexto.cpcbas` and `videoinverso.cpcbas`**: Examples using advanced control characters like transparency (`CHR$(22)`) and inverse video (`CHR$(24)`).
- **`pause.cpcbas`**: Demonstration of system pauses using `CALL &BB18` and `PAUSE 0`.
- **`movimiento.cpcbas` and `teclado.cpcbas`**: Graphical demos displaying interactive moving elements and real-time keyboard interaction.
- **`sprite.cpcbas`**: Creation of user-defined graphics with `SYMBOL`.
- **`circulos.cpcbas`, `figura3.cpcbas`, `cuadrados.cpcbas`**: Extensive graphical drawing tests (`PLOT`, `DRAW`, trigonometry).

## Credits & Thanks
- Font: [damianvila/font-cpc464](https://github.com/damianvila/font-cpc464)
- DSK Processing inspired by: [muckypaws/AmstradDSKExplorer](https://github.com/muckypaws/AmstradDSKExplorer)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
