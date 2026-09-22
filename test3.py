from core.lexer import Lexer
from core.parser import Parser
from core.interpreter import Interpreter

code = """
10 C$=CHR$(255)
20 PRINT " ";C$;:FRAME
"""
lexer = Lexer(code)
parser = Parser(lexer.tokens)
prog = parser.parse()
interpreter = Interpreter(prog)
interpreter.variables["C$"] = "2"
interpreter.execute()
