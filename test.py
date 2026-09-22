from core.interpreter import Interpreter
from core.lexer import Lexer
from core.parser import Parser

prog_code = '''
10 X1=0: X2=0: Y=200
20 C$=CHR$(65)
30 PRINT " ";C$;:FRAME
'''
l = Lexer(prog_code)
p = Parser(l.tokens)
prog = p.parse()
interpreter = Interpreter(prog)
interpreter.execute()
