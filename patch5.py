import sys

with open('video/display.py', 'r') as f:
    code = f.read()

code = code.replace('def _clear_to_end_of_line(self, win_cols):', 'def _clear_to_end_of_line(self, win_cols, stream=0):')
code = code.replace('def _clear_to_end_of_screen(self, win_cols, win_rows):', 'def _clear_to_end_of_screen(self, win_cols, win_rows, stream=0):')

code = code.replace('self._clear_to_end_of_line(win_cols)', 'self._clear_to_end_of_line(win_cols, stream)')
code = code.replace('self._clear_to_start_of_line(win_cols)', 'self._clear_to_start_of_line(win_cols, stream)')

# get_text_window() without stream inside insert_line etc
code = code.replace('left, right, top, bottom = self.get_text_window()', 'left, right, top, bottom = self.get_text_window(stream)')

with open('video/display.py', 'w') as f:
    f.write(code)
