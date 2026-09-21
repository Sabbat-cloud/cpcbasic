import sys

with open('core/parser.py', 'r') as f:
    code = f.read()

code = code.replace('''class ClsStatement(Statement):
    pass''', '''class ClsStatement(Statement):
    def __init__(self, stream=None):
        self.stream = stream''')

code = code.replace('''class LocateStatement(Statement):
    def __init__(self, col, row):
        self.col = col
        self.row = row''', '''class LocateStatement(Statement):
    def __init__(self, col, row, stream=None):
        self.col = col
        self.row = row
        self.stream = stream''')

code = code.replace('''class WindowStatement(Statement):
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom''', '''class WindowStatement(Statement):
    def __init__(self, left, right, top, bottom, stream=None):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.stream = stream''')

code = code.replace('''class PenStatement(Statement):
    def __init__(self, pen, bg_mode=None):
        self.pen = pen
        self.bg_mode = bg_mode''', '''class PenStatement(Statement):
    def __init__(self, pen, bg_mode=None, stream=None):
        self.pen = pen
        self.bg_mode = bg_mode
        self.stream = stream''')

code = code.replace('''class PaperStatement(Statement):
    def __init__(self, paper):
        self.paper = paper''', '''class PaperStatement(Statement):
    def __init__(self, paper, stream=None):
        self.paper = paper
        self.stream = stream''')

with open('core/parser.py', 'w') as f:
    f.write(code)
