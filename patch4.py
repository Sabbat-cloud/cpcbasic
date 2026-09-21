import sys
with open('core/parser.py', 'r') as f:
    code = f.read()

code = code.replace('''class ClsStatement:
    pass''', '''class ClsStatement:
    def __init__(self, stream=None):
        self.stream = stream''')

code = code.replace('''class LocateStatement:
    def __init__(self, col, row):
        self.col = col
        self.row = row''', '''class LocateStatement:
    def __init__(self, col, row, stream=None):
        self.col = col
        self.row = row
        self.stream = stream''')

code = code.replace('''class WindowStatement:
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom''', '''class WindowStatement:
    def __init__(self, left, right, top, bottom, stream=None):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.stream = stream''')

code = code.replace('''class PenStatement:
    def __init__(self, pen, bg_mode=None):
        self.pen = pen
        self.bg_mode = bg_mode''', '''class PenStatement:
    def __init__(self, pen, bg_mode=None, stream=None):
        self.pen = pen
        self.bg_mode = bg_mode
        self.stream = stream''')

code = code.replace('''class PaperStatement:
    def __init__(self, paper):
        self.paper = paper''', '''class PaperStatement:
    def __init__(self, paper, stream=None):
        self.paper = paper
        self.stream = stream''')

code = code.replace('''            elif self.current_token.value == 'WINDOW':
                self.eat(KEYWORD)
                # optionally #channel,
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression() # channel
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL) # ,
                left = self.parse_expression()''', '''            elif self.current_token.value == 'WINDOW':
                self.eat(KEYWORD)
                stream = None
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                left = self.parse_expression()''')
code = code.replace('                return WindowStatement(left, right, top, bottom)', '                return WindowStatement(left, right, top, bottom, stream)')

code = code.replace('''            elif self.current_token.value == 'LOCATE':
                self.eat(KEYWORD)
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression() # stream
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                
                col = self.parse_expression()''', '''            elif self.current_token.value == 'LOCATE':
                self.eat(KEYWORD)
                stream = None
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                
                col = self.parse_expression()''')
code = code.replace('                return LocateStatement(col, row)', '                return LocateStatement(col, row, stream)')

code = code.replace('''            elif self.current_token.value == 'PEN':
                self.eat(KEYWORD)
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression() # stream
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                pen = None''', '''            elif self.current_token.value == 'PEN':
                self.eat(KEYWORD)
                stream = None
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                pen = None''')
code = code.replace('                return PenStatement(pen, bg_mode)', '                return PenStatement(pen, bg_mode, stream)')

code = code.replace('''            elif self.current_token.value == 'PAPER':
                self.eat(KEYWORD)
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression() # stream
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                paper = self.parse_expression()
                return PaperStatement(paper)''', '''            elif self.current_token.value == 'PAPER':
                self.eat(KEYWORD)
                stream = None
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                paper = self.parse_expression()
                return PaperStatement(paper, stream)''')

code = code.replace('''            elif self.current_token.value == 'CLS':
                self.eat(KEYWORD)
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression() # stream
                return ClsStatement()''', '''            elif self.current_token.value == 'CLS':
                self.eat(KEYWORD)
                stream = None
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                return ClsStatement(stream)''')

with open('core/parser.py', 'w') as f:
    f.write(code)
