# CPCBasic Emulator

*[Read this in Spanish (Leer en Español)](README-es.md)*

CPCBasic is a high-level Amstrad CPC Locomotive BASIC interpreter written entirely in Python. Instead of emulating the Z80 hardware architecture cycle by cycle, this emulator implements a custom AST (Abstract Syntax Tree) Parser that reads pure BASIC plain-text files (`.cpcbas` or ASCII `.bas`) and executes them directly using modern software.

It uses `pygame` for highly accurate audiovisual reproduction, capturing the aesthetic feel of the classic 8-bit machine.

## Features

- **Lexical Tokenizer & AST Parser**: Full interpretation of Locomotive BASIC keywords, logic loops (`FOR`, `IF/THEN`), subroutines (`GOSUB`/`RETURN`), and mathematical functions.
- **Authentic Graphics Subsystem**: Uses the Amstrad CPC palette and supports standard hardware resolutions (`MODE 0`, `MODE 1`, `MODE 2`) with proper pixel scaling.
- **Original Pixel Font**: Integrates the original CPC464 pixel font for a 1:1 text rendering experience (`LOCATE`, `PRINT`, `PEN`, `PAPER`).
- **Procedural Audio (AY-3-8912)**: Accurately parses the `SOUND` command and generates procedural square waves and white noise in real-time via `numpy` and Pygame's mixer.
- **Keyboard Interaction**: Support for non-blocking asynchronous keyboard reading (`INKEY$`).
- **Disk (.dsk) Read Support**: On-the-fly mounting of `.dsk` files. It extracts and executes plain-text (ASCII) BASIC files stored within AMSDOS formats seamlessly.

*(Note: It does not support tokenized binary BASIC files or compiled Z80 machine code binaries since it is a high-level language interpreter, not a CPU emulator).*

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

You can also run `.dsk` images directly, provided the scripts inside are saved in ASCII format:
```bash
python main.py mydisk.dsk
```

## Examples

Check the `examples/` folder to test the capabilities:
- `matrix.cpcbas`: A visual demo of colors, arrays, random numbers, loops, and procedural sound.
- `teclado.cpcbas`: A real-time keyboard interaction loop using `INKEY$`.
- `hola.cpcbas`: A simple "Hello World" demonstrating plotting lines, moving coordinates, and changing inks.

## Credits & Thanks
- Font: [damianvila/font-cpc464](https://github.com/damianvila/font-cpc464)
- DSK Processing inspired by: [muckypaws/AmstradDSKExplorer](https://github.com/muckypaws/AmstradDSKExplorer)
