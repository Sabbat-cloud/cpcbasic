import pygame
import sys

CPC_PALETTE = [
    (0x00, 0x00, 0x00), # 0: Black
    (0x00, 0x00, 0x80), # 1: Blue
    (0x00, 0x00, 0xFF), # 2: Bright Blue
    (0x80, 0x00, 0x00), # 3: Red
    (0x80, 0x00, 0x80), # 4: Magenta
    (0x80, 0x00, 0xFF), # 5: Mauve
    (0xFF, 0x00, 0x00), # 6: Bright Red
    (0xFF, 0x00, 0x80), # 7: Purple
    (0xFF, 0x00, 0xFF), # 8: Bright Magenta
    (0x00, 0x80, 0x00), # 9: Green
    (0x00, 0x80, 0x80), # 10: Cyan
    (0x00, 0x80, 0xFF), # 11: Sky Blue
    (0x80, 0x80, 0x00), # 12: Yellow
    (0x80, 0x80, 0x80), # 13: White (Grey)
    (0x80, 0x80, 0xFF), # 14: Pastel Blue
    (0xFF, 0x80, 0x00), # 15: Orange
    (0xFF, 0x80, 0x80), # 16: Pink
    (0xFF, 0x80, 0xFF), # 17: Pastel Magenta
    (0x00, 0xFF, 0x00), # 18: Bright Green
    (0x00, 0xFF, 0x80), # 19: Sea Green
    (0x00, 0xFF, 0xFF), # 20: Bright Cyan
    (0x80, 0xFF, 0x00), # 21: Lime
    (0x80, 0xFF, 0x80), # 22: Pastel Green
    (0x80, 0xFF, 0xFF), # 23: Pastel Cyan
    (0xFF, 0xFF, 0x00), # 24: Bright Yellow
    (0xFF, 0xFF, 0x80), # 25: Pastel Yellow
    (0xFF, 0xFF, 0xFF), # 26: Bright White
]

class Display:
    def __init__(self, width=640, height=400, scale=2):
        pygame.init()
        self.logical_width = width
        self.logical_height = height
        self.scale = scale
        
        self.border_size_logical = 32
        self.screen_width = (self.logical_width + 2 * self.border_size_logical) * self.scale
        self.screen_height = (self.logical_height + 2 * self.border_size_logical) * self.scale
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Amstrad CPC BASIC Emulator")
        
        self.logical_surface = pygame.Surface((self.logical_width, self.logical_height), depth=8)
        
        self.mode = 1
        
        self.border_color1 = 1
        self.border_color2 = None
        
        self.inks = [1, 24, 20, 6, 26, 0, 2, 8, 10, 12, 14, 16, 18, 22, 1, 16]
        self.flash_inks = [None] * 16
        self.flash_inks[14] = 24
        self.flash_inks[15] = 11
        
        self.current_pen = 1
        self.current_paper = 0
        
        self._update_palette(False)
        self.logical_surface.fill(self.current_paper)
        
        self.origin_x = 0
        self.origin_y = 0
        self.graphics_x = 0
        self.graphics_y = 0
        
        pygame.font.init()
        try:
            self.font = pygame.font.Font('assets/cpc464.ttf', 16)
        except Exception:
            self.font = pygame.font.SysFont('courier', 16, bold=True)
            
        self.text_col = 1
        self.text_row = 1
        
        self.key_buffer = []
        self.tag_active = False

        self.user_symbols = {
            240: [8, 28, 62, 127, 8, 8, 8, 8],
            241: [8, 8, 8, 8, 127, 62, 28, 8],
            242: [8, 12, 14, 15, 14, 12, 8, 0],
            243: [16, 48, 112, 240, 112, 48, 16, 0],
            250: [24, 24, 24, 126, 24, 24, 36, 66],
            251: [24, 24, 90, 60, 24, 24, 36, 66],
            252: [24, 24, 24, 60, 90, 24, 36, 66],
        }

    def _update_palette(self, flash_state):
        palette = [(0,0,0)] * 256
        for i in range(16):
            if flash_state and self.flash_inks[i] is not None:
                palette[i] = CPC_PALETTE[self.flash_inks[i]]
            else:
                palette[i] = CPC_PALETTE[self.inks[i]]
        self.logical_surface.set_palette(palette)

    def define_symbol(self, char_code, matrix):
        if 0 <= char_code <= 255 and len(matrix) == 8:
            self.user_symbols[char_code] = matrix

    def set_mode(self, mode):
        if mode in (0, 1, 2):
            self.mode = mode
            self.inks = [1, 24, 20, 6, 26, 0, 2, 8, 10, 12, 14, 16, 18, 22, 1, 16]
            self.flash_inks = [None] * 16
            self.flash_inks[14] = 24
            self.flash_inks[15] = 11
            self.current_pen = 1
            self.current_paper = 0
            self._update_palette(False)
            self.logical_surface.fill(self.current_paper)
            self.update()

    def set_ink(self, pen, color, color2=None):
        if 0 <= pen < 16 and 0 <= color < 27:
            self.inks[pen] = color
            if color2 is not None and 0 <= color2 < 27:
                self.flash_inks[pen] = color2
            else:
                self.flash_inks[pen] = None

    def set_border(self, color, color2=None):
        if 0 <= color < 27:
            self.border_color1 = color
            if color2 is not None and 0 <= color2 < 27:
                self.border_color2 = color2
            else:
                self.border_color2 = None

    def set_pen(self, pen):
        if 0 <= pen < 16:
            self.current_pen = pen

    def set_paper(self, paper):
        if 0 <= paper < 16:
            self.current_paper = paper

    def get_text_window(self):
        if hasattr(self, 'text_window') and self.text_window is not None:
            return self.text_window
        return (1, self.get_max_cols(), 1, 25)

    def set_window(self, left, right, top, bottom):
        self.text_window = (left, right, top, bottom)
        self.locate(1, 1)

    def clear_graphics(self):
        left, right, top, bottom = self.get_text_window()
        max_cols = self.get_max_cols()
        char_width = self.logical_width // max_cols
        char_height = 16
        
        px = (left - 1) * char_width
        py = (top - 1) * char_height
        pw = (right - left + 1) * char_width
        ph = (bottom - top + 1) * char_height
        
        rect = pygame.Rect(px, py, pw, ph)
        pygame.draw.rect(self.logical_surface, self.current_paper, rect)
        self.locate(1, 1)
        
    def locate(self, col, row):
        self.text_col = col
        self.text_row = row

    def get_max_cols(self):
        if self.mode == 0: return 20
        elif self.mode == 1: return 40
        else: return 80

    def print_text(self, text):
        max_cols = self.get_max_cols()
        char_width = self.logical_width // max_cols
        char_height = 16
        
        left, right, top, bottom = self.get_text_window()
        win_cols = right - left + 1
        win_rows = bottom - top + 1
        
        for char in str(text):
            if char == '\n':
                self.text_col = 1
                self.text_row += 1
            else:
                char_code = ord(char)
                
                if self.tag_active:
                    x, y = self._cpc_to_screen(self.graphics_x, self.graphics_y)
                    y -= char_height
                else:
                    abs_col = left + self.text_col - 1
                    abs_row = top + self.text_row - 1
                    x = (abs_col - 1) * char_width
                    y = (abs_row - 1) * char_height
                
                char_surface = None
                if hasattr(self, 'user_symbols') and char_code in self.user_symbols:
                    matrix = self.user_symbols[char_code]
                    char_surface = pygame.Surface((8, 8))
                    char_surface.fill((0,0,0))
                    for r, row_val in enumerate(matrix):
                        for c in range(8):
                            if row_val & (1 << (7 - c)):
                                char_surface.set_at((c, r), (255,255,255))
                    char_surface = pygame.transform.scale(char_surface, (char_width, char_height))
                else:
                    try:
                        char_surface = self.font.render(char, False, (255,255,255), (0,0,0))
                        char_surface = pygame.transform.scale(char_surface, (char_width, char_height))
                    except pygame.error:
                        pass
                
                if char_surface is not None:
                    with pygame.PixelArray(self.logical_surface) as pxarray:
                        with pygame.PixelArray(char_surface) as char_px:
                            for cy in range(char_height):
                                for cx in range(char_width):
                                    px_x = x + cx
                                    px_y = y + cy
                                    if 0 <= px_x < self.logical_width and 0 <= px_y < self.logical_height:
                                        if char_px[cx, cy] & 0xFFFFFF > 0x7FFFFF:
                                            pxarray[px_x, px_y] = self.current_pen
                                        else:
                                            pxarray[px_x, px_y] = self.current_paper
                
                if self.tag_active:
                    self.graphics_x += char_width
                else:
                    self.text_col += 1
                
            if self.text_col > win_cols:
                self.text_col = 1
                self.text_row += 1
                
            if self.text_row > win_rows:
                px = (left - 1) * char_width
                py = (top - 1) * char_height
                pw = win_cols * char_width
                ph = win_rows * char_height
                
                subsurface = self.logical_surface.subsurface(pygame.Rect(px, py, pw, ph))
                subsurface.scroll(0, -char_height)
                
                bottom_rect = pygame.Rect(px, py + ph - char_height, pw, char_height)
                pygame.draw.rect(self.logical_surface, self.current_paper, bottom_rect)
                
                self.text_row = win_rows
                
    def _cpc_to_screen(self, x, y):
        screen_x = self.origin_x + x
        screen_y = self.logical_height - 1 - (self.origin_y + y)
        return int(screen_x), int(screen_y)

    def move(self, x, y):
        self.graphics_x = x
        self.graphics_y = y

    def plot(self, x, y, pen=None):
        if pen is None:
            pen = self.current_pen
        self.move(x, y)
        sx, sy = self._cpc_to_screen(x, y)
        
        if self.mode == 0:
            pw, ph = 4, 2
        elif self.mode == 1:
            pw, ph = 2, 2
        else:
            pw, ph = 1, 2
            
        rect = pygame.Rect(sx, sy, pw, ph)
        pygame.draw.rect(self.logical_surface, pen, rect)

    def draw(self, x, y, pen=None):
        if pen is None:
            pen = self.current_pen
            
        start_x, start_y = self._cpc_to_screen(self.graphics_x, self.graphics_y)
        end_x, end_y = self._cpc_to_screen(x, y)
        
        if self.mode == 0: width = 4
        elif self.mode == 1: width = 2
        else: width = 1
            
        pygame.draw.line(self.logical_surface, pen, (start_x, start_y), (end_x, end_y), width)
        self.move(x, y)

    def fill(self, pen=None):
        if pen is None:
            pen = self.current_pen
        start_x, start_y = self._cpc_to_screen(self.graphics_x, self.graphics_y)
        if start_x < 0 or start_x >= self.logical_width or start_y < 0 or start_y >= self.logical_height:
            return
            
        target_pen = self.logical_surface.get_at_mapped((start_x, start_y))
        if target_pen == pen:
            return
            
        queue = [(start_x, start_y)]
        visited = set()
        
        while queue:
            x, y = queue.pop(0)
            if (x, y) in visited: continue
            visited.add((x, y))
            
            if self.logical_surface.get_at_mapped((x, y)) == target_pen:
                self.logical_surface.set_at((x, y), pen)
                if x > 0: queue.append((x-1, y))
                if x < self.logical_width - 1: queue.append((x+1, y))
                if y > 0: queue.append((x, y-1))
                if y < self.logical_height - 1: queue.append((x, y+1))

    def test(self, x, y):
        sx, sy = self._cpc_to_screen(x, y)
        if 0 <= sx < self.logical_width and 0 <= sy < self.logical_height:
            return self.logical_surface.get_at_mapped((sx, sy))
        return 0

    def get_inkey_str(self):
        self.process_events()
        if self.key_buffer:
            return self.key_buffer.pop(0)
        return ""

    def update(self):
        flash_state = (pygame.time.get_ticks() // 300) % 2 == 1
        self._update_palette(flash_state)
        
        active_border = self.border_color2 if flash_state and self.border_color2 is not None else self.border_color1
        self.screen.fill(CPC_PALETTE[active_border])
        
        scaled_surface = pygame.transform.scale(self.logical_surface, (self.logical_width * self.scale, self.logical_height * self.scale))
        self.screen.blit(scaled_surface, (self.border_size_logical * self.scale, self.border_size_logical * self.scale))
        pygame.display.flip()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode:
                    self.key_buffer.append(event.unicode)

    def input_string(self):
        input_str = ""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.print_text('\n')
                        self.update()
                        return input_str
                    elif event.key == pygame.K_BACKSPACE:
                        if len(input_str) > 0:
                            input_str = input_str[:-1]
                            self.text_col -= 1
                            if self.text_col < 1:
                                self.text_col = self.get_max_cols()
                                self.text_row -= 1
                            self.print_text(' ')
                            self.text_col -= 1
                            if self.text_col < 1:
                                self.text_col = self.get_max_cols()
                                self.text_row -= 1
                            self.update()
                    elif event.unicode and ord(event.unicode) >= 32:
                        input_str += event.unicode
                        self.print_text(event.unicode)
                        self.update()
            pygame.time.wait(10)
