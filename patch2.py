import sys

with open('video/display.py', 'r') as f:
    code = f.read()

# Fix current_pen in print_text
code = code.replace('''                            if row_val & (1 << (7 - c)):
                                pygame.draw.rect(self.logical_surface, self.current_pen, (px + c * (char_width // 8), py + r * (char_height // 8), char_width // 8, char_height // 8))
                            elif self.bg_mode == 0:
                                pygame.draw.rect(self.logical_surface, self.current_paper, (px + c * (char_width // 8), py + r * (char_height // 8), char_width // 8, char_height // 8))''', '''                            if row_val & (1 << (7 - c)):
                                pen = self.streams[stream]['pen'] if hasattr(self, 'streams') and stream in self.streams else self.current_pen
                                pygame.draw.rect(self.logical_surface, pen, (px + c * (char_width // 8), py + r * (char_height // 8), char_width // 8, char_height // 8))
                            elif self.bg_mode == 0:
                                paper = self.streams[stream]['paper'] if hasattr(self, 'streams') and stream in self.streams else self.current_paper
                                pygame.draw.rect(self.logical_surface, paper, (px + c * (char_width // 8), py + r * (char_height // 8), char_width // 8, char_height // 8))''')

with open('video/display.py', 'w') as f:
    f.write(code)

