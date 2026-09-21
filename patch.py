import sys

with open('video/display.py', 'r') as f:
    code = f.read()

code = code.replace('self.text_col = 1\n        self.text_row = 1', "self.streams = {i: {'text_col': 1, 'text_row': 1, 'text_window': None, 'paper': 0, 'pen': 1} for i in range(8)}")

code = code.replace('''    def get_text_window(self):
        if hasattr(self, 'text_window') and self.text_window is not None:
            return self.text_window
        return (1, self.get_max_cols(), 1, 25)''', '''    def get_text_window(self, stream=0):
        if hasattr(self, 'streams') and stream in self.streams and self.streams[stream]['text_window'] is not None:
            return self.streams[stream]['text_window']
        return (1, self.get_max_cols(), 1, 25)''')

code = code.replace('''    def set_window(self, left, right, top, bottom):
        self.text_window = (left, right, top, bottom)
        self.locate(1, 1)''', '''    def set_window(self, left, right, top, bottom, stream=0):
        if not hasattr(self, 'streams'): self.streams = {i: {'text_col': 1, 'text_row': 1, 'text_window': None, 'paper': 0, 'pen': 1} for i in range(8)}
        if stream not in self.streams: self.streams[stream] = {'text_col': 1, 'text_row': 1, 'text_window': None, 'paper': self.current_paper, 'pen': self.current_pen}
        self.streams[stream]['text_window'] = (left, right, top, bottom)
        self.locate(1, 1, stream)''')

code = code.replace('''    def locate(self, col, row):
        self.text_col = col
        self.text_row = row''', '''    def locate(self, col, row, stream=0):
        if not hasattr(self, 'streams'): self.streams = {i: {'text_col': 1, 'text_row': 1, 'text_window': None, 'paper': 0, 'pen': 1} for i in range(8)}
        if stream not in self.streams: self.streams[stream] = {'text_col': 1, 'text_row': 1, 'text_window': None, 'paper': self.current_paper, 'pen': self.current_pen}
        self.streams[stream]['text_col'] = col
        self.streams[stream]['text_row'] = row''')

code = code.replace('''    def set_pen(self, pen):
        if 0 <= pen < 16:
            self.current_pen = pen''', '''    def set_pen(self, pen, stream=0):
        if 0 <= pen < 16:
            self.current_pen = pen
            if hasattr(self, 'streams') and stream in self.streams: self.streams[stream]['pen'] = pen''')

code = code.replace('''    def set_paper(self, paper):
        if 0 <= paper < 16:
            self.current_paper = paper''', '''    def set_paper(self, paper, stream=0):
        if 0 <= paper < 16:
            self.current_paper = paper
            if hasattr(self, 'streams') and stream in self.streams: self.streams[stream]['paper'] = paper''')

code = code.replace('''    def clear_graphics(self):
        left, right, top, bottom = self.get_text_window()''', '''    def clear_graphics(self, stream=0):
        left, right, top, bottom = self.get_text_window(stream)''')

code = code.replace('''pygame.draw.rect(self.logical_surface, self.current_paper, rect)''', '''paper = self.streams[stream]['paper'] if hasattr(self, 'streams') and stream in self.streams else self.current_paper
        pygame.draw.rect(self.logical_surface, paper, rect)''')

code = code.replace('def _clear_area(self, start_col, end_col, start_row, end_row):', 'def _clear_area(self, start_col, end_col, start_row, end_row, stream=0):')
code = code.replace('def _clear_to_start_of_screen(self, win_cols, win_rows):', 'def _clear_to_start_of_screen(self, win_cols, win_rows, stream=0):')
code = code.replace('def _clear_to_start_of_line(self, win_cols):', 'def _clear_to_start_of_line(self, win_cols, stream=0):')
code = code.replace('def _insert_line(self, win_cols, win_rows):', 'def _insert_line(self, win_cols, win_rows, stream=0):')
code = code.replace('def _delete_line(self, win_cols, win_rows):', 'def _delete_line(self, win_cols, win_rows, stream=0):')
code = code.replace('def _delete_char(self, win_cols):', 'def _delete_char(self, win_cols, stream=0):')
code = code.replace('def print_text(self, text):', 'def print_text(self, text, stream=0):')

import re
code = re.sub(r'(?<!\.)self\.text_col', r'self.streams[stream]["text_col"]', code)
code = re.sub(r'(?<!\.)self\.text_row', r'self.streams[stream]["text_row"]', code)

with open('video/display.py', 'w') as f:
    f.write(code)

