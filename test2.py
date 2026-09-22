from core.lexer import Lexer
from core.parser import Parser
from core.interpreter import Interpreter
import pygame
pygame.init()

code = """
10 CLS:TAG:EVERY 10 GOSUB 90
20 X1=RND*320: X2=RND*320
30 Y=200+RND*200:C$=CHR$(RND*255)
40 FOR X=320-X1 TO 320+X2 STEP 4
50 DI
60 MOVE 320,0,1:MOVE X-2,Y:MOVE X,Y
70 PRINT " ";C$;:FRAME
80 EI:NEXT:GOTO 20
90 MOVE 320,0:DRAW X+8,Y-16,0:RETURN
"""

lexer = Lexer(code)
parser = Parser(lexer.tokens)
prog = parser.parse()
interpreter = Interpreter(prog, scale=1)

# Initialize
if interpreter.line_numbers:
    interpreter.pc = interpreter.line_numbers[0]
    interpreter.running = True

for _ in range(500):
    if not interpreter.running: break
    if interpreter.pc == 70:
        print(f"PRINTING C$: {repr(interpreter.variables.get('C$'))}")
    interpreter.step()
