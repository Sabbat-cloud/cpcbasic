from core.lexer import Lexer

code = """
10 MODE 1
20 PRINT "HELLO WORLD"
30 FOR I=1 TO 10
40 PRINT I
50 NEXT I
60 GOTO 20 ' LOOPS FOREVER
"""

lexer = Lexer(code)
for token in lexer.tokens:
    if token.type != 'NEWLINE':
        print(token)
