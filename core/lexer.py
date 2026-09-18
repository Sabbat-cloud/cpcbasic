import re

EOF = 'EOF'
NUMBER = 'NUMBER'
HEX_NUMBER = 'HEX_NUMBER'
STRING = 'STRING'
IDENTIFIER = 'IDENTIFIER'
KEYWORD = 'KEYWORD'
SYMBOL = 'SYMBOL'
NEWLINE = 'NEWLINE'

KEYWORDS = {
    'PRINT', 'GOTO', 'GOSUB', 'RETURN', 'IF', 'THEN', 'ELSE',
    'FOR', 'TO', 'STEP', 'NEXT', 'WHILE', 'WEND', 'DIM', 'LET',
    'MODE', 'PEN', 'PAPER', 'INK', 'BORDER', 'PLOT', 'DRAW', 'DRAWR', 'MOVE', 'MOVER', 'ORIGIN',
    'SOUND', 'ENV', 'ENT', 'CALL', 'LOAD', 'SAVE', 'RUN', 'LIST', 'NEW',
    'AND', 'OR', 'XOR', 'NOT', 'MOD', 'DEFINT', 'DEFREAL', 'DEFSTR',
    'LOCATE', 'CLS', 'CLG', 'CLEAR', 'END', 'STOP', 'DATA', 'READ', 'RESTORE',
    'REM', 'INPUT', 'SYMBOL', 'FRAME', 'MASK', 'ZONE', 'WINDOW', 'TRON', 'TROFF', 'TAG', 'TAGOFF',
    'ON', 'LEN', 'BREAK', 'CONT', 'SPEED', 'XPOS', 'YPOS', 'VPOS',
    'RANDOMIZE', 'DEG', 'RAD', 'FILL'
}

token_specification = [
    ('HEX_NUMBER', r'&[0-9A-Fa-f]+'),      
    ('NUMBER',   r'\d+(\.\d*)?([eE][+-]?\d+)?'), 
    ('STRING',   r'".*?"'),                
    ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*[%!\$]?'), 
    ('SYMBOL',   r'<=|>=|<>|[=<>\+\-\*/\^\\\(\),:;\?]'), 
    ('NEWLINE',  r'\n'),                   
    ('SKIP',     r'[ \t\r]+'),               
    ('MISMATCH', r'.'),                    
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {self.value!r}, Line: {self.line}, Col: {self.column})'

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        line_num = 1
        line_start = 0
        
        # Split by lines to handle REM properly
        lines = self.code.split('\n')
        
        for line_num_zero, line_code in enumerate(lines):
            line_num = line_num_zero + 1
            line_start = 0
            
            # Check for REM or ' comment
            rem_match = re.search(r'\bREM\b', line_code, re.IGNORECASE)
            tick_match = line_code.find("'")
            
            comment_start = -1
            if rem_match:
                comment_start = rem_match.start()
            if tick_match != -1 and (comment_start == -1 or tick_match < comment_start):
                comment_start = tick_match
                
            code_to_parse = line_code if comment_start == -1 else line_code[:comment_start]
            
            for mo in re.finditer(tok_regex, code_to_parse, re.IGNORECASE):
                kind = mo.lastgroup
                value = mo.group()
                column = mo.start()
                
                if kind == 'NUMBER':
                    pass
                elif kind == 'IDENTIFIER':
                    if value.upper() in KEYWORDS:
                        kind = 'KEYWORD'
                        value = value.upper()
                elif kind == 'STRING':
                    value = value[1:-1] 
                elif kind == 'SKIP':
                    continue
                elif kind == 'MISMATCH':
                    # Si encontramos caracteres de control binarios al principio, 
                    # probablemente sea un archivo BASIC tokenizado
                    if ord(value) < 32 and value not in ('\n', '\r', '\t'):
                        raise RuntimeError(
                            f"ERROR FATAL: Se ha encontrado el byte binario {repr(value)} en la línea {line_num}.\n\n"
                            "Esto significa que el archivo .BAS está guardado en formato TOKENIZADO (binario comprimido del Amstrad) "
                            "y no en formato de texto ASCII. Además, los juegos comerciales suelen contener "
                            "un cargador BASIC que carga código máquina Z80 (.BIN) usando CALL &XXXX.\n\n"
                            "Nuestro emulador es un Intérprete de BASIC de alto nivel en Python, no un "
                            "emulador a nivel de hardware del procesador Z80, por lo que no puede ejecutar "
                            "juegos comerciales precompilados. Solo admite scripts de BASIC puro en texto plano."
                        )
                    raise RuntimeError(f'{value!r} unexpected on line {line_num}')
                
                self.tokens.append(Token(kind, value, line_num, column))
                
            # Treat comment as a token if needed, but usually we just skip it
            if comment_start != -1:
                pass # Skipping comment
            
            # Add newline token to separate statements, unless it's the last line and empty
            self.tokens.append(Token(NEWLINE, '\n', line_num, len(line_code)))

        self.tokens.append(Token(EOF, '', line_num, 0))
