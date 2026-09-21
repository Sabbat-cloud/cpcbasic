import sys

with open('core/interpreter.py', 'r') as f:
    code = f.read()

code = code.replace('''                elif isinstance(stmt, LocateStatement):
                    col = int(self.evaluate(stmt.col))
                    row = int(self.evaluate(stmt.row)) if stmt.row else None
                    if row is not None:
                        self.display.locate(col, row)
                    else:
                        self.display.locate(col, self.display.text_row)''', '''                elif isinstance(stmt, LocateStatement):
                    col = int(self.evaluate(stmt.col))
                    row = int(self.evaluate(stmt.row)) if getattr(stmt, 'row', None) else None
                    stream = int(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) else 0
                    if row is not None:
                        self.display.locate(col, row, stream)
                    else:
                        self.display.locate(col, self.display.streams[stream]['text_row'] if hasattr(self.display, 'streams') else self.display.text_row, stream)''')

code = code.replace('''                elif isinstance(stmt, ClsStatement):
                    self.display.clear_graphics()
                    self.display.locate(1, 1)''', '''                elif isinstance(stmt, ClsStatement):
                    stream = int(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) else 0
                    self.display.clear_graphics(stream)
                    self.display.locate(1, 1, stream)''')

code = code.replace('''                elif isinstance(stmt, WindowStatement):
                    left = int(self.evaluate(stmt.left))
                    right = int(self.evaluate(stmt.right))
                    top = int(self.evaluate(stmt.top))
                    bottom = int(self.evaluate(stmt.bottom))
                    if hasattr(self.display, 'set_window'):
                        self.display.set_window(left, right, top, bottom)''', '''                elif isinstance(stmt, WindowStatement):
                    left = int(self.evaluate(stmt.left))
                    right = int(self.evaluate(stmt.right))
                    top = int(self.evaluate(stmt.top))
                    bottom = int(self.evaluate(stmt.bottom))
                    stream = int(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) else 0
                    if hasattr(self.display, 'set_window'):
                        self.display.set_window(left, right, top, bottom, stream)''')

code = code.replace('''                elif isinstance(stmt, PenStatement):
                    if stmt.pen is not None:
                        pen = int(self.evaluate(stmt.pen))
                        self.display.set_pen(pen)''', '''                elif isinstance(stmt, PenStatement):
                    if stmt.pen is not None:
                        pen = int(self.evaluate(stmt.pen))
                        stream = int(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) else 0
                        self.display.set_pen(pen, stream)''')

code = code.replace('''                elif isinstance(stmt, PaperStatement):
                    paper = int(self.evaluate(stmt.paper))
                    self.display.set_paper(paper)''', '''                elif isinstance(stmt, PaperStatement):
                    paper = int(self.evaluate(stmt.paper))
                    stream = int(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) else 0
                    self.display.set_paper(paper, stream)''')

code = code.replace('''                    if isinstance(stmt.stream, int) and stmt.stream == 8:
                        self.display.print_text(out_str + ("\n" if newline else ""))
                    else:
                        self.display.print_text(out_str + ("\n" if newline else ""))''', '''                    stream = int(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) is not None else 0
                    if getattr(stmt, 'stream', None) is not None and isinstance(stmt.stream, int) and stmt.stream == 8:
                        self.display.print_text(out_str + ("\n" if newline else ""), 0)
                    else:
                        self.display.print_text(out_str + ("\n" if newline else ""), stream)''')

with open('core/interpreter.py', 'w') as f:
    f.write(code)

