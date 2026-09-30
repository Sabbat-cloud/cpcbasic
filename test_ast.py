from core.lexer import Lexer
from core.parser import Parser

with open('examples/musicaysonidos/musica1.cpcbas', 'r') as f:
    code = f.read()

lexer = Lexer(code)
parser = Parser(lexer.tokens)
program = parser.parse()

for line_num in sorted(program.lines.keys()):
    print(f"Line {line_num}:")
    for stmt in program.lines[line_num]:
        print(f"  {stmt}")
