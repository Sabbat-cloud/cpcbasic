from core.lexer import Lexer
from core.parser import Parser
from core.interpreter import Interpreter

code = """
10 READ a, b, c
20 DATA &X11, &H10, &10
"""
l = Lexer(code)
p = Parser(l.tokens)
i = Interpreter()
i.load(p.statements)
i.run(headless=True) # or just run step by step
print("Variables:", i.variables)
