# CPCBasic Emulator

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Amstrad CPC](https://img.shields.io/badge/Platform-Amstrad_CPC-red.svg)
![Locomotive BASIC](https://img.shields.io/badge/Language-Locomotive_BASIC-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
*[Read this in Spanish (Leer en Español)](README-es.md)*

CPCBasic is a high-level Amstrad CPC Locomotive BASIC interpreter written entirely in Python. Instead of emulating the Z80 hardware architecture cycle by cycle, this emulator implements a custom AST (Abstract Syntax Tree) Parser that reads pure BASIC plain-text files (`.cpcbas` or ASCII `.bas`) and executes them directly using modern software.

It uses `pygame` for highly accurate audiovisual reproduction, capturing the aesthetic feel of the classic 8-bit machine.

## Features

- **Lexical Tokenizer & AST Parser**: Full interpretation of Locomotive BASIC keywords. The `core/parser.py` module implements a Recursive Descent Parser that converts the token sequence into an Abstract Syntax Tree (AST). It robustly handles Amstrad's complex syntax: multiple statements per line separated by colons (`:`), nested loops, `IF/THEN/ELSE` conditions, complex mathematical operations, expressions, and system-exclusive statements like interrupts and memory management.
- **Math & String Functions**: 100% mathematical coverage of the Amstrad standard (`ATN`, `SIN`, `COS`, `TAN`, `PI`, `SQR`, `INT`, `FIX`, `ROUND`, `CINT`, `CREAL`, `UNT`, `LOG`, `MAX`, `MIN`, `EXP`, `SGN`) and extensive string support (`CHR$`, `COPYCHR$`, `LEFT$`, `UPPER$`, `STR$`, `SPACE$`, `STRING$`, `HEX$`, `BIN$`, `INSTR`, `DEC$`).
- **Advanced Terminal Control**: Full support for control characters via `CHR$()`, enabling line feeds, cursor movements (`CHR$(11)`), transparency and text overprinting (`CHR$(22)`), and inverse video/ink swapping (`CHR$(24)`).
- **Authentic Graphics Subsystem**: Uses the standard Amstrad CPC firmware color palette and supports hardware resolutions (`MODE 0`, `MODE 1`, `MODE 2`). It implements graphical commands such as `PLOT`, `DRAW`, `MOVE`, `ORIGIN`, and `CLG`.
- **String & Terminal Output**: Properly handles `PRINT` statements with separators (`,`, `;`), along with stream support (`#`).
- **Original Pixel Font**: Integrates the original CPC464 pixel font for a 1:1 text rendering experience (`LOCATE`, `PRINT`, `PEN`, `PAPER`).
- **Procedural Audio (AY-3-8912)**: Accurately parses the `SOUND` command and generates procedural square waves and white noise in real-time via `numpy` and Pygame's mixer.
- **Keyboard & Joystick Interaction**: Support for asynchronous keyboard reading (`INKEY$`, `INKEY`), hardware pauses (`CALL &BB18`, `PAUSE 0`), and simulated joysticks using Pygame (`JOY`).
- **Hybrid Emulation Architecture (Memory & Z80)**: Implements a 64KB virtual RAM array with bidirectional video-memory synchronization. `PEEK` and `POKE` commands operating on the CRTC memory area (`&C000` to `&FFFF`) will dynamically read and write pixels directly to the PyGame display, perfectly mimicking the Amstrad hardware layout. Furthermore, a "Ghost Z80" register system (`_REG_A`, `_REG_HL`, etc.) is exposed to the user, allowing BASIC variables to directly alter the virtual CPU state before executing firmware `CALL` instructions.
- **Disk (.dsk) Read Support**: On-the-fly mounting of `.dsk` files. Seamlessly extracts and executes plain-text (ASCII) BASIC files stored within AMSDOS formats.
- **Optimized Execution & Speed Control**: Features cached AST code generation for incredibly fast unlimited execution, while offering an optional speed throttle to replicate the original Amstrad CPC 6128 CPU speed.

*(Note: It does not support tokenized binary BASIC files or raw compiled Z80 machine code binaries, as it is a high-level interpreter rather than a cycle-accurate CPU emulator. However, it does intercept standard Amstrad ROM firmware `CALL`s and emulates their behavior natively in Python using the virtual Z80 registers).*

**⚠️ WARNING: This emulator is in an early stage of development. Many features might fail.**

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

You can run the emulator by passing a BASIC script as an argument. The window is scaled x2 by default, but you can change it with `--scale`. You can also control the execution speed with the `--speed` parameter (use `real` for original hardware speed or `unlimited` for maximum speed).

```bash
python main.py examples/matrix.cpcbas --scale 3 --speed real
```

You can also run `.dsk` images directly:
```bash
python main.py mydisk.dsk
```

## Complete Examples

Check the `examples/` folder to test the capabilities of the emulator. Some of the over 20 included examples are:
- **`matrix.cpcbas`**: Matrix effect demonstrating the use of colors, random numbers, loops, and procedural sound.
- **`juego_reflejos.cpcbas`**: A complete game with asynchronous timers (`AFTER`/`EVERY`), volume/tone envelopes, direct keyboard reading (`INKEY`), and complex screen handling.
- **`demo_colores.cpcbas`**: Border and ink color cycling using logical timers.
- **`subrrayadotexto.cpcbas` and `videoinverso.cpcbas`**: Examples using advanced control characters like transparency (`CHR$(22)`) and inverse video (`CHR$(24)`).
- **`pause.cpcbas`**: Demonstration of system pauses using `CALL &BB18` and `PAUSE 0`.
- **`movimiento.cpcbas` and `teclado.cpcbas`**: Graphical demos interacting with the keyboard buffer in real-time.
- **`sprite.cpcbas`**: Creation of user-defined graphics with `SYMBOL`.
- **`circulos.cpcbas`, `figura3.cpcbas`, `cuadrados.cpcbas`**: Extensive graphical drawing tests (`PLOT`, `DRAW`, trigonometric math).
- **`tecnicasproggraficos/`**: Inside `examples/` you will find plenty of examples, including the full listing of all programs from the book *"Técnicas de programación gráfica"* in `examples/tecnicasproggraficos/`.
- **Official Manual Examples**: Thanks to the latest updates in string and math variables, most simple examples from the *Locomotive BASIC User Guide* can be tested directly (for example, by pasting them into `temp_run.cpcbas`) and will work out of the box.

## Why?

The short answer is for fun. I grew up with Amstrad CPC BASIC and sometimes wanted to try out small things, whether out of nostalgia or curiosity, and being able to access BASIC without having to load a full emulator environment felt practical.
You can edit program listings with whichever editor you prefer without relying on an emulator, mounting disk drives, etc.
Random file access is currently supported, allowing us to read, write, and modify any file on our PC to process it with our BASIC programs.
Of course, there is also the absence of memory limitations and the speed boost.
Its most obvious limitation is the lack of full machine code execution. However, thanks to the new Hybrid Architecture, standard firmware calls (like `CALL &BB5A`, `CALL &BB18`) are intercepted. You can manipulate the virtual Z80 CPU registers directly from BASIC using special variables (e.g. `_REG_A = 65`) before calling the firmware, and the Python engine will simulate the hardware response instantly, reading your registers and executing the routine!

## Credits & Thanks
- Font: [damianvila/font-cpc464](https://github.com/damianvila/font-cpc464)
- DSK Processing inspired by: [muckypaws/AmstradDSKExplorer](https://github.com/muckypaws/AmstradDSKExplorer)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
