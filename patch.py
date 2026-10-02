import re

with open('video/display.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """                active_pen = self.streams[stream]['pen'] if hasattr(self, 'streams') and stream in self.streams else self.current_pen
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
                                        pxarray[px_x, px_y] = active_paper"""

replacement = """                if self.tag_active:
                    active_pen = self.graphics_pen
                    active_paper = self.graphics_paper
                    is_transparent = (self.bg_mode == 1)
                else:
                    active_pen = self.streams[stream]['pen'] if hasattr(self, 'streams') and stream in self.streams else self.current_pen
                    active_paper = self.streams[stream]['paper'] if hasattr(self, 'streams') and stream in self.streams else self.current_paper
                    is_transparent = self.transparent_text

                if char_surface is not None:
                    with pygame.PixelArray(self.logical_surface) as pxarray:
                        for cy in range(char_height):
                            for cx in range(char_width):
                                px_x = x + cx
                                px_y = y + cy
                                if 0 <= px_x < self.logical_width and 0 <= px_y < self.logical_height:
                                    color = char_surface.get_at((cx, cy))
                                    plot_pen = None
                                    if color.r > 127:
                                        plot_pen = active_pen
                                    elif not is_transparent:
                                        plot_pen = active_paper
                                    
                                    if plot_pen is not None:
                                        if self.tag_active and self.graphics_write_mode != 0:
                                            curr = pxarray[px_x, px_y]
                                            if self.graphics_write_mode == 1:
                                                pxarray[px_x, px_y] = curr ^ plot_pen
                                            elif self.graphics_write_mode == 2:
                                                pxarray[px_x, px_y] = curr & plot_pen
                                            elif self.graphics_write_mode == 3:
                                                pxarray[px_x, px_y] = curr | plot_pen
                                        else:
                                            pxarray[px_x, px_y] = plot_pen"""

if target in content:
    content = content.replace(target, replacement)
    with open('video/display.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced successfully")
else:
    print("Target not found. Let's find similar lines...")
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'active_pen = self.streams' in line:
            print(f"Line {i}: {line.strip()}")
