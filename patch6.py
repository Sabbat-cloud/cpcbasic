import sys

with open('video/display.py', 'r') as f:
    code = f.read()

code = code.replace('self.set_paper(char_code % 16)', 'self.set_paper(char_code % 16, stream)')
code = code.replace('self.set_pen(char_code % 16)', 'self.set_pen(char_code % 16, stream)')
code = code.replace('self.locate(max(1, min(win_cols, self.esc_args[0])), max(1, min(win_rows, self.esc_args[1])))', 'self.locate(max(1, min(win_cols, self.esc_args[0])), max(1, min(win_rows, self.esc_args[1])), stream)')
code = code.replace('self.clear_graphics() # Text clear', 'self.clear_graphics(stream) # Text clear')

code = code.replace('tmp = self.current_pen; self.current_pen = self.current_paper; self.current_paper = tmp', '''if hasattr(self, 'streams') and stream in self.streams:
                        tmp = self.streams[stream]['pen']
                        self.streams[stream]['pen'] = self.streams[stream]['paper']
                        self.streams[stream]['paper'] = tmp
                    else:
                        tmp = self.current_pen; self.current_pen = self.current_paper; self.current_paper = tmp''')

with open('video/display.py', 'w') as f:
    f.write(code)
