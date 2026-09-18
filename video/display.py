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
        
        # Physical window
        self.screen = pygame.display.set_mode((self.logical_width * self.scale, self.logical_height * self.scale))
        pygame.display.set_caption("Amstrad CPC BASIC Emulator")
        
        # Logical surface where everything is drawn
        self.logical_surface = pygame.Surface((self.logical_width, self.logical_height))
        
        self.mode = 1
        
        # Inks map logical pens (0-15) to hardware colors (0-26)
        # Default Locomotive BASIC palette for 16 pens:
        self.inks = [1, 24, 20, 6, 26, 0, 2, 8, 10, 12, 14, 16, 18, 22, 24, 16]
        
        self.current_pen = 1
        self.current_paper = 0
        
        # Initialize background color
        self.logical_surface.fill(CPC_PALETTE[self.inks[0]])
        
        # Origin for graphics (bottom left by default: 0, 0)
        self.origin_x = 0
        self.origin_y = 0
        self.graphics_x = 0
        self.graphics_y = 0
        
        # Text variables
        pygame.font.init()
        try:
            self.font = pygame.font.Font('assets/cpc464.ttf', 16)
        except Exception as e:
            print(f"Warning: Could not load CPC font, using default. {e}")
            self.font = pygame.font.SysFont('courier', 16, bold=True)
            
        self.text_col = 1
        self.text_row = 1
        
        self.key_buffer = []
        self.tag_active = False

        self.user_symbols = {
            240: [8, 28, 62, 127, 8, 8, 8, 8],      # Flecha Arriba
            241: [8, 8, 8, 8, 127, 62, 28, 8],      # Flecha Abajo
            242: [8, 12, 14, 15, 14, 12, 8, 0],     # Flecha Izquierda
            243: [16, 48, 112, 240, 112, 48, 16, 0],# Flecha Derecha
            250: [24, 24, 24, 126, 24, 24, 36, 66], # Muñeco brazos horizontales
            251: [24, 24, 90, 60, 24, 24, 36, 66],  # Muñeco brazos arriba
            252: [24, 24, 24, 60, 90, 24, 36, 66],  # Muñeco brazos abajo
        }

    def define_symbol(self, char_code, matrix):
        if 0 <= char_code <= 255 and len(matrix) == 8:
            self.user_symbols[char_code] = matrix

    def set_mode(self, mode):
        if mode in (0, 1, 2):
            self.mode = mode
            self.inks = [1, 24, 20, 6, 26, 0, 2, 8, 10, 12, 14, 16, 18, 22, 24, 16]
            self.current_pen = 1
            self.current_paper = 0
            self.logical_surface.fill(CPC_PALETTE[self.inks[self.current_paper]])
            self.update()

    def set_ink(self, pen, color):
        if 0 <= pen < 16 and 0 <= color < 27:
            self.inks[pen] = color

    def set_pen(self, pen):
        if 0 <= pen < 16:
            self.current_pen = pen

    def set_paper(self, paper):
        if 0 <= paper < 16:
            self.current_paper = paper

    def clear_graphics(self):
        self.logical_surface.fill(CPC_PALETTE[self.inks[self.current_paper]])
        
    def locate(self, col, row):
        self.text_col = col
        self.text_row = row

    def get_max_cols(self):
        if self.mode == 0: return 20
        elif self.mode == 1: return 40
        else: return 80

    def print_text(self, text):
        fg_color = CPC_PALETTE[self.inks[self.current_pen]]
        bg_color = CPC_PALETTE[self.inks[self.current_paper]]
        
        max_cols = self.get_max_cols()
        char_width = self.logical_width // max_cols
        char_height = 16 # 400 / 25 rows
        
        for char in str(text):
            if char == '\n':
                self.text_col = 1
                self.text_row += 1
            else:
                char_code = ord(char)
                
                if self.tag_active:
                    # In graphics mode (TAG), origin is bottom-left relative to window or custom origin
                    x, y = self._cpc_to_screen(self.graphics_x, self.graphics_y)
                    # Text renders from top-left, so we might need to adjust y
                    y -= char_height
                else:
                    x = (self.text_col - 1) * char_width
                    y = (self.text_row - 1) * char_height
                
                if hasattr(self, 'user_symbols') and char_code in self.user_symbols:
                    matrix = self.user_symbols[char_code]
                    char_surface = pygame.Surface((8, 8))
                    char_surface.fill(bg_color)
                    for r, row_val in enumerate(matrix):
                        for c in range(8):
                            if row_val & (1 << (7 - c)):
                                char_surface.set_at((c, r), fg_color)
                    char_surface = pygame.transform.scale(char_surface, (char_width, char_height))
                    self.logical_surface.blit(char_surface, (x, y))
                else:
                    try:
                        char_surface = self.font.render(char, False, fg_color, bg_color)
                        char_surface = pygame.transform.scale(char_surface, (char_width, char_height))
                        self.logical_surface.blit(char_surface, (x, y))
                    except pygame.error:
                        pass # Ignore zero-width characters or rendering errors
                
                if self.tag_active:
                    self.graphics_x += char_width # CPC coordinates advance right
                else:
                    self.text_col += 1
                
            if self.text_col > max_cols:
                self.text_col = 1
                self.text_row += 1
                
            if self.text_row > 25:
                self.logical_surface.scroll(0, -char_height)
                rect = pygame.Rect(0, self.logical_height - char_height, self.logical_width, char_height)
                pygame.draw.rect(self.logical_surface, bg_color, rect)
                self.text_row = 25
                
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
        color = CPC_PALETTE[self.inks[pen]]
        
        if self.mode == 0:
            pw, ph = 4, 2
        elif self.mode == 1:
            pw, ph = 2, 2
        else:
            pw, ph = 1, 2
            
        rect = pygame.Rect(sx, sy, pw, ph)
        pygame.draw.rect(self.logical_surface, color, rect)

    def draw(self, x, y, pen=None):
        if pen is None:
            pen = self.current_pen
            
        start_x, start_y = self._cpc_to_screen(self.graphics_x, self.graphics_y)
        end_x, end_y = self._cpc_to_screen(x, y)
        color = CPC_PALETTE[self.inks[pen]]
        
        if self.mode == 0: width = 4
        elif self.mode == 1: width = 2
        else: width = 1
            
        pygame.draw.line(self.logical_surface, color, (start_x, start_y), (end_x, end_y), width)
        self.move(x, y)

    def fill(self, pen=None):
        if pen is None:
            pen = self.current_pen
        start_x, start_y = self._cpc_to_screen(self.graphics_x, self.graphics_y)
        if start_x < 0 or start_x >= self.logical_width or start_y < 0 or start_y >= self.logical_height:
            return
            
        target_color = self.logical_surface.get_at((start_x, start_y))
        fill_color = pygame.Color(*CPC_PALETTE[self.inks[pen]])
        if target_color == fill_color:
            return
            
        # Basic BFS flood fill
        queue = [(start_x, start_y)]
        visited = set()
        
        # We need to lock the surface for fast pixel access, but pygame.surfarray is better
        # For simplicity, we just use get_at and set_at, though it can be slow
        while queue:
            x, y = queue.pop(0)
            if (x, y) in visited: continue
            visited.add((x, y))
            
            if self.logical_surface.get_at((x, y)) == target_color:
                self.logical_surface.set_at((x, y), fill_color)
                if x > 0: queue.append((x-1, y))
                if x < self.logical_width - 1: queue.append((x+1, y))
                if y > 0: queue.append((x, y-1))
                if y < self.logical_height - 1: queue.append((x, y+1))

    def get_inkey_str(self):
        self.process_events()
        if self.key_buffer:
            return self.key_buffer.pop(0)
        return ""

    def update(self):
        # Scale logical surface to physical window
        scaled_surface = pygame.transform.scale(self.logical_surface, (self.logical_width * self.scale, self.logical_height * self.scale))
        self.screen.blit(scaled_surface, (0, 0))
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

