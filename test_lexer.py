from core.lexer import Lexer
from core.parser import Parser
l=Lexer('10 PRINT " "+CHR$(8)')
print(l.tokens)
p=Parser(l.tokens)
prog=p.parse()
print(vars(prog.lines[10][0].expressions[1]))
