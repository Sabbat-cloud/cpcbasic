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
        # Activar la repetición automática de teclas para que INKEY$ detecte teclas mantenidas
        pygame.key.set_repeat(300, 50)
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
        self.graphics_pen = 1
        self.graphics_paper = 0
        self.bg_mode = 0
        
        self.speed_ink_1 = 10 * 20  # 200ms
        self.speed_ink_2 = 10 * 20  # 200ms
        
        self.line_mask = 255
        self.mask_first = 1
        
        self.esc_state = 0
        self.esc_cmd = ''
        self.esc_args = []
        self.transparent_text = False
        
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
            
        self.streams = {i: {'text_col': 1, 'text_row': 1, 'text_window': None, 'paper': 0, 'pen': 1} for i in range(8)}
        self.text_buffer = [[' ' for _ in range(80)] for _ in range(25)]
        
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

    def set_pen(self, pen, stream=0):
        if 0 <= pen < 16:
            self.current_pen = pen
            if hasattr(self, 'streams') and stream in self.streams: self.streams[stream]['pen'] = pen

    def set_paper(self, paper, stream=0):
        if 0 <= paper < 16:
            self.current_paper = paper
            if hasattr(self, 'streams') and stream in self.streams: self.streams[stream]['paper'] = paper

    def set_graphics_pen(self, pen):
        if 0 <= pen < 16:
            self.graphics_pen = pen
            
    def set_graphics_paper(self, paper):
        if 0 <= paper < 16:
            self.graphics_paper = paper
            
    def set_bg_mode(self, mode):
        if mode in (0, 1):
            self.bg_mode = mode

    def set_mask(self, mask):
        self.line_mask = mask & 255

    def set_mask_first(self, first):
        self.mask_first = 1 if first else 0

    def get_text_window(self, stream=0):
        if hasattr(self, 'streams') and stream in self.streams and self.streams[stream]['text_window'] is not None:
            return self.streams[stream]['text_window']
        return (1, self.get_max_cols(), 1, 25)

    def set_window(self, left, right, top, bottom, stream=0):
        if not hasattr(self, 'streams'): self.streams = {i: {'text_col': 1, 'text_row': 1, 'text_window': None, 'paper': 0, 'pen': 1} for i in range(8)}
        if stream not in self.streams: self.streams[stream] = {'text_col': 1, 'text_row': 1, 'text_window': None, 'paper': self.current_paper, 'pen': self.current_pen}
        self.streams[stream]['text_window'] = (left, right, top, bottom)
        self.locate(1, 1, stream)

    def clear_graphics(self, stream=0):
        left, right, top, bottom = self.get_text_window(stream)
        max_cols = self.get_max_cols()
        char_width = self.logical_width // max_cols
        char_height = 16
        
        px = (left - 1) * char_width
        py = (top - 1) * char_height
        pw = (right - left + 1) * char_width
        ph = (bottom - top + 1) * char_height
        
        rect = pygame.Rect(px, py, pw, ph)
        paper = self.streams[stream]['paper'] if hasattr(self, 'streams') and stream in self.streams else self.current_paper
        pygame.draw.rect(self.logical_surface, paper, rect)
        
        for r in range(top - 1, bottom):
            for c in range(left - 1, right):
                if 0 <= r < 25 and 0 <= c < 80:
                    self.text_buffer[r][c] = ' '
                    
        self.locate(1, 1)

    def copychr(self, stream=0):
        left, right, top, bottom = self.get_text_window(stream)
        abs_col = left + self.streams[stream]["text_col"] - 1
        abs_row = top + self.streams[stream]["text_row"] - 1
        if 0 <= abs_row - 1 < 25 and 0 <= abs_col - 1 < 80:
            return self.text_buffer[abs_row - 1][abs_col - 1]
        return ' '
        
    def locate(self, col, row, stream=0):
        if not hasattr(self, 'streams'): self.streams = {i: {'text_col': 1, 'text_row': 1, 'text_window': None, 'paper': 0, 'pen': 1} for i in range(8)}
        if stream not in self.streams: self.streams[stream] = {'text_col': 1, 'text_row': 1, 'text_window': None, 'paper': self.current_paper, 'pen': self.current_pen}
        self.streams[stream]['text_col'] = col
        self.streams[stream]['text_row'] = row

    def get_max_cols(self):
        if self.mode == 0: return 20
        elif self.mode == 1: return 40
        else: return 80

    def _clear_area(self, start_col, end_col, start_row, end_row, stream=0):
        left, right, top, bottom = self.get_text_window(stream)
        max_cols = self.get_max_cols()
        char_width = self.logical_width // max_cols
        char_height = 16
        
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                px = (left + c - 2) * char_width
                py = (top + r - 2) * char_height
                rect = pygame.Rect(px, py, char_width, char_height)
                paper = self.streams[stream]['paper'] if hasattr(self, 'streams') and stream in self.streams else self.current_paper
                pygame.draw.rect(self.logical_surface, paper, rect)
                abs_c = left + c - 2
                abs_r = top + r - 2
                if 0 <= abs_r < 25 and 0 <= abs_c < 80:
                    self.text_buffer[abs_r][abs_c] = ' '

    def _clear_to_end_of_line(self, win_cols, stream=0):
        self._clear_area(self.streams[stream]["text_col"], win_cols, self.streams[stream]["text_row"], self.streams[stream]["text_row"])

    def _clear_to_start_of_line(self, win_cols, stream=0):
        self._clear_area(1, self.streams[stream]["text_col"], self.streams[stream]["text_row"], self.streams[stream]["text_row"])

    def _clear_to_end_of_screen(self, win_cols, win_rows, stream=0):
        self._clear_to_end_of_line(win_cols, stream)
        if self.streams[stream]["text_row"] < win_rows:
            self._clear_area(1, win_cols, self.streams[stream]["text_row"] + 1, win_rows)

    def _clear_to_start_of_screen(self, win_cols, win_rows, stream=0):
        self._clear_to_start_of_line(win_cols, stream)
        if self.streams[stream]["text_row"] > 1:
            self._clear_area(1, win_cols, 1, self.streams[stream]["text_row"] - 1)

    def _insert_line(self, win_cols, win_rows, stream=0):
        if self.streams[stream]["text_row"] > win_rows: return
        left, right, top, bottom = self.get_text_window(stream)
        max_cols = self.get_max_cols()
        char_width = self.logical_width // max_cols
        char_height = 16
        px = (left - 1) * char_width
        py = (top + self.streams[stream]["text_row"] - 2) * char_height
        pw = win_cols * char_width
        ph = (win_rows - self.streams[stream]["text_row"] + 1) * char_height
        sub = self.logical_surface.subsurface(pygame.Rect(px, py, pw, ph))
        sub.scroll(0, char_height)
        self._clear_area(1, win_cols, self.streams[stream]["text_row"], self.streams[stream]["text_row"])

    def _delete_line(self, win_cols, win_rows, stream=0):
        if self.streams[stream]["text_row"] > win_rows: return
        left, right, top, bottom = self.get_text_window(stream)
        max_cols = self.get_max_cols()
        char_width = self.logical_width // max_cols
        char_height = 16
        px = (left - 1) * char_width
        py = (top + self.streams[stream]["text_row"] - 2) * char_height
        pw = win_cols * char_width
        ph = (win_rows - self.streams[stream]["text_row"] + 1) * char_height
        sub = self.logical_surface.subsurface(pygame.Rect(px, py, pw, ph))
        sub.scroll(0, -char_height)
        self._clear_area(1, win_cols, win_rows, win_rows)

    def _delete_char(self, win_cols, stream=0):
        if self.streams[stream]["text_col"] > win_cols: return
        left, right, top, bottom = self.get_text_window(stream)
        max_cols = self.get_max_cols()
        char_width = self.logical_width // max_cols
        char_height = 16
        px = (left + self.streams[stream]["text_col"] - 2) * char_width
        py = (top + self.streams[stream]["text_row"] - 2) * char_height
        pw = (win_cols - self.streams[stream]["text_col"] + 1) * char_width
        sub = self.logical_surface.subsurface(pygame.Rect(px, py, pw, char_height))
        sub.scroll(-char_width, 0)
        self._clear_area(win_cols, win_cols, self.streams[stream]["text_row"], self.streams[stream]["text_row"])

    def print_text(self, text, stream=0):
        max_cols = self.get_max_cols()
        char_width = self.logical_width // max_cols
        char_height = 16
        
        left, right, top, bottom = self.get_text_window(stream)
        win_cols = right - left + 1
        win_rows = bottom - top + 1
        
        for char in str(text):
            char_code = ord(char)
            
            if self.esc_state > 0:
                # We reuse esc_state for multi-byte VDU commands
                if self.esc_state == 14: # PAPER
                    self.set_paper(char_code % 16, stream)
                    self.esc_state = 0
                elif self.esc_state == 15: # PEN
                    self.set_pen(char_code % 16, stream)
                    self.esc_state = 0
                elif self.esc_state == 22: # Transparent mode
                    self.transparent_text = (char_code != 0)
                    self.esc_state = 0
                elif self.esc_state == 31: # LOCATE
                    self.esc_args.append(char_code)
                    if len(self.esc_args) == 2:
                        self.locate(max(1, min(win_cols, self.esc_args[0])), max(1, min(win_rows, self.esc_args[1])), stream)
                        self.esc_state = 0
                continue
                
            if char_code < 32:
                if char_code == 7: # BEL
                    continue
                elif char_code == 8: # BS (Left)
                    self.streams[stream]["text_col"] = max(1, self.streams[stream]["text_col"] - 1)
                elif char_code == 9: # TAB (Right)
                    self.streams[stream]["text_col"] = min(win_cols, self.streams[stream]["text_col"] + 1)
                elif char_code == 10: # LF (Down)
                    self.streams[stream]["text_row"] += 1
                    if self.streams[stream]["text_row"] > win_rows: self.streams[stream]["text_row"] = win_rows
                elif char_code == 11: # VT (Up)
                    self.streams[stream]["text_row"] = max(1, self.streams[stream]["text_row"] - 1)
                elif char_code == 12: # FF (Clear Window)
                    self.clear_graphics(stream) # Text clear
                elif char_code == 13: # CR (Left edge)
                    self.streams[stream]["text_col"] = 1
                elif char_code == 14: # Set Paper
                    self.esc_state = 14
                elif char_code == 15: # Set Pen
                    self.esc_state = 15
                elif char_code == 22: # Set Transparent mode
                    self.esc_state = 22
                elif char_code == 24: # CAN (Inverse Video)
                    if hasattr(self, 'streams') and stream in self.streams:
                        tmp = self.streams[stream]['pen']
                        self.streams[stream]['pen'] = self.streams[stream]['paper']
                        self.streams[stream]['paper'] = tmp
                    else:
                        tmp = self.current_pen; self.current_pen = self.current_paper; self.current_paper = tmp
                elif char_code == 31: # US (Locate)
                    self.esc_state = 31
                    self.esc_args = []
                # Rest of control codes ignored
                continue
            else:
                
                if self.tag_active:
                    x, y = self._cpc_to_screen(self.graphics_x, self.graphics_y)
                    y -= char_height
                else:
                    abs_col = left + self.streams[stream]["text_col"] - 1
                    abs_row = top + self.streams[stream]["text_row"] - 1
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
                
                active_pen = self.streams[stream]['pen'] if hasattr(self, 'streams') and stream in self.streams else self.current_pen
                active_paper = self.streams[stream]['paper'] if hasattr(self, 'streams') and stream in self.streams else self.current_paper

                if char_surface is not None:
                    with pygame.PixelArray(self.logical_surface) as pxarray:
                        for cy in range(char_height):
                            for cx in range(char_width):
                                px_x = x + cx
                                px_y = y + cy
                                if 0 <= px_x < self.logical_width and 0 <= px_y < self.logical_height:
                                    color = char_surface.get_at((cx, cy))
                                    if color.r > 127:
                                        pxarray[px_x, px_y] = active_pen
                                    elif not self.transparent_text:
                                        pxarray[px_x, px_y] = active_paper
                
                if self.tag_active:
                    self.graphics_x += char_width
                else:
                    if 0 <= abs_row - 1 < 25 and 0 <= abs_col - 1 < 80:
                        self.text_buffer[abs_row - 1][abs_col - 1] = char
                    self.streams[stream]["text_col"] += 1
                
            if self.streams[stream]["text_col"] > win_cols:
                self.streams[stream]["text_col"] = 1
                self.streams[stream]["text_row"] += 1
                
            if self.streams[stream]["text_row"] > win_rows:
                px = (left - 1) * char_width
                py = (top - 1) * char_height
                pw = win_cols * char_width
                ph = win_rows * char_height
                
                subsurface = self.logical_surface.subsurface(pygame.Rect(px, py, pw, ph))
                subsurface.scroll(0, -char_height)
                
                bottom_rect = pygame.Rect(px, py + ph - char_height, pw, char_height)
                paper = self.streams[stream]['paper'] if hasattr(self, 'streams') and stream in self.streams else self.current_paper
                pygame.draw.rect(self.logical_surface, paper, bottom_rect)
                
                self.streams[stream]["text_row"] = win_rows
                
    def _cpc_to_screen(self, x, y):
        screen_x = self.origin_x + x
        screen_y = self.logical_height - 1 - (self.origin_y + y)
        return int(screen_x), int(screen_y)

    def move(self, x, y):
        self.graphics_x = x
        self.graphics_y = y

    def plot(self, x, y, pen=None):
        if pen is None:
            pen = self.graphics_pen
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
            pen = self.graphics_pen
            
        start_x, start_y = self._cpc_to_screen(self.graphics_x, self.graphics_y)
        end_x, end_y = self._cpc_to_screen(x, y)
        
        if self.mode == 0: width = 4
        elif self.mode == 1: width = 2
        else: width = 1
        
        if self.line_mask == 255 and self.mask_first == 1:
            pygame.draw.line(self.logical_surface, pen, (start_x, start_y), (end_x, end_y), width)
        else:
            dx = abs(end_x - start_x)
            dy = abs(end_y - start_y)
            sx = 1 if start_x < end_x else -1
            sy = 1 if start_y < end_y else -1
            err = dx - dy
            
            cx, cy = start_x, start_y
            bit_idx = 7
            first = True
            
            while True:
                draw_dot = False
                if first:
                    draw_dot = (self.mask_first == 1)
                    first = False
                else:
                    draw_dot = (self.line_mask & (1 << bit_idx)) != 0
                    bit_idx = (bit_idx - 1) % 8
                    
                if draw_dot:
                    rect = pygame.Rect(cx, cy, width, 2)
                    pygame.draw.rect(self.logical_surface, pen, rect)
                elif self.bg_mode == 0:
                    rect = pygame.Rect(cx, cy, width, 2)
                    pygame.draw.rect(self.logical_surface, self.graphics_paper, rect)
                    
                if cx == end_x and cy == end_y:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    cx += sx
                if e2 < dx:
                    err += dx
                    cy += sy
                    
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

    def get_inkey_state(self, cpc_key):
        self.process_events()
        keys = pygame.key.get_pressed()
        
        # Mapeo de teclas de hardware del Amstrad CPC a Pygame
        # Valores extraídos de 'varios.pdf' Parte 5: Esquemas del teclado
        cpc_to_pygame = {
            # Teclas especiales
            47: pygame.K_SPACE,
            18: pygame.K_RETURN,
            14: pygame.K_KP_ENTER,
            66: pygame.K_ESCAPE,
            16: pygame.K_BACKSPACE, # DEL en CPC
            15: pygame.K_DELETE,    # CLR en CPC
            
            # Cursores
            0:  pygame.K_UP,
            2:  pygame.K_DOWN,
            8:  pygame.K_LEFT,
            1:  pygame.K_RIGHT,
            
            # Joystick 0 (a menudo leído vía INKEY en juegos)
            72: pygame.K_UP,
            73: pygame.K_DOWN,
            74: pygame.K_LEFT,
            75: pygame.K_RIGHT,
            76: pygame.K_x,     # Fire 1
            77: pygame.K_z,     # Fire 2
        }
        
        if cpc_key in cpc_to_pygame:
            return 0 if keys[cpc_to_pygame[cpc_key]] else -1
        return -1

    def set_speed_ink(self, time1, time2):
        self.speed_ink_1 = max(1, time1 * 20)
        self.speed_ink_2 = max(1, time2 * 20)

    def _get_screen(self, num):
        if num == 1:
            return self.logical_surface
        if not hasattr(self, 'extra_screens'):
            self.extra_screens = {}
        if num not in self.extra_screens:
            self.extra_screens[num] = pygame.Surface((self.logical_width, self.logical_height))
            self.extra_screens[num].fill(self.current_paper)
        return self.extra_screens[num]

    def _set_screen(self, num, surface):
        if num == 1:
            self.logical_surface = surface
        else:
            if not hasattr(self, 'extra_screens'):
                self.extra_screens = {}
            self.extra_screens[num] = surface

    def screencopy(self, dest, src, section=None):
        src_surf = self._get_screen(src)
        dest_surf = self._get_screen(dest)
        if section is None:
            dest_surf.blit(src_surf, (0, 0))
        else:
            # CPC screen has 16KB. 1/64 is 256 bytes. We map it to horizontal slices.
            slice_h = max(1, self.logical_height // 64)
            y = section * slice_h
            rect = pygame.Rect(0, y, self.logical_width, slice_h)
            dest_surf.blit(src_surf, (0, y), rect)

    def screenswap(self, s1, s2, section=None):
        if section is None:
            surf1 = self._get_screen(s1)
            surf2 = self._get_screen(s2)
            self._set_screen(s1, surf2)
            self._set_screen(s2, surf1)
        else:
            # For a section, we must copy back and forth
            surf1 = self._get_screen(s1)
            surf2 = self._get_screen(s2)
            slice_h = max(1, self.logical_height // 64)
            y = section * slice_h
            rect = pygame.Rect(0, y, self.logical_width, slice_h)
            tmp = pygame.Surface((self.logical_width, slice_h))
            tmp.blit(surf1, (0, 0), rect)
            surf1.blit(surf2, (0, y), rect)
            surf2.blit(tmp, (0, y))

    def update(self):
        total_time = self.speed_ink_1 + self.speed_ink_2
        current_phase = pygame.time.get_ticks() % total_time
        flash_state = current_phase >= self.speed_ink_1
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

    def clear_input(self):
        self.key_buffer.clear()
        pygame.event.clear(pygame.KEYDOWN)
        pygame.event.clear(pygame.KEYUP)

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
                            self.streams[stream]["text_col"] -= 1
                            if self.streams[stream]["text_col"] < 1:
                                self.streams[stream]["text_col"] = self.get_max_cols()
                                self.streams[stream]["text_row"] -= 1
                            self.print_text(' ')
                            self.streams[stream]["text_col"] -= 1
                            if self.streams[stream]["text_col"] < 1:
                                self.streams[stream]["text_col"] = self.get_max_cols()
                                self.streams[stream]["text_row"] -= 1
                            self.update()
                    elif event.unicode and ord(event.unicode) >= 32:
                        input_str += event.unicode
                        self.print_text(event.unicode)
                        self.update()
            pygame.time.wait(10)
