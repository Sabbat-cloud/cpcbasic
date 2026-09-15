import pygame
import sys

CPC_PALETTE = [
    (0x04, 0x04, 0x04), (0x80, 0x80, 0x80), (0xff, 0xff, 0xff), # 0-2
    (0x80, 0x00, 0x00), (0xff, 0x00, 0x00), (0xff, 0x80, 0x80), # 3-5
    (0xff, 0x7f, 0x00), (0xff, 0xff, 0x80), (0xff, 0xff, 0x00), # 6-8
    (0x80, 0x80, 0x00), (0x00, 0x80, 0x00), (0x01, 0xff, 0x00), # 9-11
    (0x80, 0xff, 0x00), (0x80, 0xff, 0x80), (0x01, 0xff, 0x80), # 12-14
    (0x00, 0x80, 0x80), (0x01, 0xff, 0xff), (0x80, 0xff, 0xff), # 15-17
    (0x00, 0x80, 0xff), (0x00, 0x00, 0xff), (0x00, 0x00, 0x7f), # 18-20
    (0x7f, 0x00, 0xff), (0x80, 0x80, 0xff), (0xff, 0x80, 0xff), # 21-23
    (0xff, 0x00, 0xff), (0xff, 0x00, 0x80), (0x80, 0x00, 0x80)  # 24-26
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
        self.inks = [0] * 16
        self.inks[0] = 1 # Grey/Blue
        self.inks[1] = 24 # Yellow
        self.inks[2] = 20 # Cyan
        self.inks[3] = 6  # Red
        
        self.current_pen = 1
        self.current_paper = 0
        
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

    def set_mode(self, mode):
        if mode in (0, 1, 2):
            self.mode = mode
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
                # Render character
                char_surface = self.font.render(char, False, fg_color, bg_color)
                char_surface = pygame.transform.scale(char_surface, (char_width, char_height))
                
                x = (self.text_col - 1) * char_width
                y = (self.text_row - 1) * char_height
                
                self.logical_surface.blit(char_surface, (x, y))
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
