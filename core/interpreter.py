import math
import random
import sys
import time
import pygame
import ast
from core.parser import (Program, PrintStatement, WriteStatement, LetStatement, GotoStatement, 
                         ModeStatement, ForStatement, NextStatement, Literal, Variable,
                         PlotStatement, DrawStatement, DrawrStatement, MoveStatement, MoverStatement, InkStatement,
                         PenStatement, PaperStatement, SoundStatement, LocateStatement, 
                         ClsStatement, ClgStatement, RawExpression, IfStatement, GosubStatement, 
                         ReturnStatement, DimStatement, EndStatement, OriginStatement,
                         DataStatement, ReadStatement, RestoreStatement,
                         InputStatement, SymbolStatement, SymbolAfterStatement, FrameStatement,
                         StopStatement, WindowStatement, WhileStatement, WendStatement,
                         OnStatement, BorderStatement, ClearStatement, ClearInputStatement, RandomizeStatement,
                         DegStatement, RadStatement, EnvStatement, EntStatement,
                         MaskStatement, ZoneStatement, SpeedStatement, TagStatement, TagoffStatement,
                         FillStatement, EraseStatement, EveryStatement, AfterStatement, LetArrayStatement, PokeStatement,
                         RsxStatement, OnErrorStatement, ErrorStatement, ResumeStatement, OnBreakStatement, OnSqStatement, CallStatement, ReleaseStatement, OutStatement, WaitStatement, CursorStatement, PlotrStatement, WidthStatement, WindowSwapStatement, ListStatement, SwapStatement, AutoStatement, CatStatement, ChainStatement, DeleteStatement, EditStatement, MemoryStatement, MergeStatement, RenumStatement, SaveStatement, LoadStatement, KeyStatement, KeyDefStatement)
from core.cpc_format import format_cpc_field, format_cpc_using
from video.display import Display
from audio.sound import SoundEngine

def cpc_chr(x): return chr(int(x))
def cpc_asc(x): return ord(x[0]) if x else 0
def cpc_rnd(x=None): return random.random()

from core.machine import Z80Registers

class BasicErrorInterrupt(Exception):
    pass


class Interpreter:

    def reset(self):
        self.variables = {}
        self.arrays = {}
        self.for_loops = {}
        self.for_stack = []
        self.gosub_stack = []
        if hasattr(self, 'while_stack'):
            self.while_stack = []
        self.timers = {0: None, 1: None, 2: None, 3: None}
        self.sq_targets = {0: 0, 1: 0, 2: 0}
        if hasattr(self, 'sound'):
            self.sound.reset()
        self.data_values = []
        self.data_ptr = 0
        self.user_functions = {}
        self.default_types = {chr(c): 'REAL' for c in range(ord('A'), ord('Z')+1)}
        self.interrupts_enabled = True
        self.angle_mode = 'RAD'
        self.tag_active = False
        self.zone_width = 13
        self.printer_width = 132
        self.printer_pos = 1
        self.file_out_pos = 1
        self.err_code = 0
        self.err_line = 0
        self.next_stmt_idx = 0
        self.virtual_time_us = 0
        self.frame_virtual_time_us = 0
        self.time_offset = 0
        self.last_sync_real_time = None
        self.last_sync_virt_us = 0
        if hasattr(self, 'restore_statements'):
            del self.restore_statements
        if hasattr(self, 'display'):
            import pygame
            if pygame.display.get_surface() is None:
                pygame.display.init()
                self.display.screen = pygame.display.set_mode((self.display.screen_width, self.display.screen_height))
            if hasattr(self.display, 'reset'):
                self.display.reset()
            else:
                self.display.set_mode(1)
            self.display.clear_input()

    def __init__(self, program, scale=2, speed='unlimited'):
        self.program = program
        self.speed = speed
        self.variables = {}
        self.arrays = {}
        self.pc = None
        self.running = False
        self.display = Display(scale=scale)
        self.display.interpreter = self
        self.sound = SoundEngine()
        self.display.sound = self.sound
        self.sq_targets = {0: 0, 1: 0, 2: 0}
        self._ppi_port_a = 0
        self._psg_selected_reg = 0
        self.virtual_time_us = 0
        self.frame_virtual_time_us = 0
        self.time_offset = 0
        self.last_sync_real_time = None
        self.last_sync_virt_us = 0
        
        # Z80 Ghost Registers
        self.z80 = Z80Registers()
        
        self.firmware_hooks = {
            0xBB03: self.fw_km_reset,
            0xBB5A: self.fw_txt_output,
            0xBB60: self.fw_txt_rd_char,
            0xBB18: self.fw_km_wait_char,
            0xBB06: self.fw_km_wait_char,
            0xBB75: self.fw_txt_set_cursor,
            0xBB78: self.fw_txt_get_cursor,
            0xBB7B: lambda: self.display.set_cursor(None, 1) if hasattr(self.display, 'set_cursor') else None,
            0xBB7E: lambda: self.display.set_cursor(None, 0) if hasattr(self.display, 'set_cursor') else None,
            0xBB81: lambda: self.display.set_cursor(1, None) if hasattr(self.display, 'set_cursor') else None,
            0xBB84: lambda: self.display.set_cursor(0, None) if hasattr(self.display, 'set_cursor') else None,
            0xBB90: self.fw_txt_set_pen,
            0xBB96: self.fw_txt_set_paper,
            0xBBC0: self.fw_gra_move_absolute,
            0xBBF6: self.fw_gra_line_absolute,
            0xBBDE: self.fw_gra_set_pen,
            0xBC0E: self.fw_scr_set_mode,
            0xBC11: self.fw_scr_get_mode,
            0xBC32: self.fw_scr_set_ink,
            0xBC38: self.fw_scr_set_border,
            0xBB24: self.fw_km_get_joystick,
            0xBCA7: self.fw_sound_reset,
            0xBCAA: self.fw_sound_queue,
            0xBCAD: self.fw_sound_check,
            0xBCB0: self.fw_sound_arm_event,
            0xBCB3: self.fw_sound_release,
            0xBCB6: self.fw_sound_hold,
            0xBCB9: self.fw_sound_continue,
            0xBCBC: self.fw_sound_ampl_envelope,
            0xBCBF: self.fw_sound_tone_envelope,
            0xBCC2: self.fw_sound_a_address,
            0xBCC5: self.fw_sound_t_address,
            0xBD34: self.fw_mc_sound_register,
            0xBD19: self.fw_mc_wait_flyback,
            0xBD1C: self.fw_mc_set_mode,
            0xBC05: self.fw_scr_set_offset,
            0xBC14: self.fw_scr_clear,
            0xBC59: self.fw_scr_access
        }
        
        self.line_numbers = sorted(list(self.program.lines.keys())) if self.program else []
        self.for_loops = {}
        self.for_stack = []
        self.gosub_stack = []
        self.timers = {0: None, 1: None, 2: None, 3: None}
        self.data_values = []
        self.data_ptr = 0
        self.user_functions = {}
        self.default_types = {chr(c): 'REAL' for c in range(ord('A'), ord('Z')+1)}
        self.interrupts_enabled = True
        
        self.angle_mode = 'RAD'
        self.tag_active = False
        self.zone_width = 13
        self.printer_width = 132
        self.printer_pos = 1
        self.file_out_pos = 1
        
        self.err_code = 0
        self.err_line = 0
        self.error_handler_line = 0
        
        # Virtual 64KB RAM for PEEK/POKE
        self.ram = bytearray(65536)
        self.init_font_ram()
        
        # Bank RAM for RSX
        self.bank_record_length = 255
        self.bank_current_record = 0
        self.bank_memory = bytearray(65536)

        # Funciones built-in del Amstrad BASIC para el evaluador
        self.builtins = {
            "__builtins__": {},
            "SIN": self.builtin_sin,
            "COS": self.builtin_cos,
            "TAN": self.builtin_tan,
            "INT": math.floor,
            "ABS": abs,
            "RND": self.cpc_rnd,
            "PI": math.pi,
            "TIME": self.get_cpc_time,
            "XPOS": lambda *args: self.display.graphics_x,
            "YPOS": lambda *args: self.display.graphics_y,
            "POS": lambda stream=0: self.get_stream_pos(stream),
            "VPOS": lambda stream=0: self.get_stream_vpos(stream),
            "CHR_STR": lambda x: chr(self.cint(x) & 0xFF),
            "ASC": cpc_asc,
            "SQR": self.builtin_sqr,
            "LOG": self.builtin_log,
            "LOG10": self.builtin_log10,
            "HIMEM": lambda: 42597,
            "VAL": lambda x: float(x) if '.' in str(x) else int(x) if str(x).lstrip('-').isdigit() else 0,
            "RIGHT_STR": lambda s, n: s[-self.cint(n):] if self.cint(n) > 0 else "",
            "MID_STR": lambda s, start, n=None: s[self.cint(start)-1:self.cint(start)-1+self.cint(n)] if n is not None else s[self.cint(start)-1:],
            "LOWER_STR": lambda s: s.lower(),
            "MAX": max,
            "SQ": self.function_sq,
            "LEN": len,
            "TEST": lambda x, y: self.display.test(self.cint(x), self.cint(y)) if hasattr(self.display, 'test') else 0,
            "TESTR": lambda x, y: self.display.test(self.display.graphics_x + self.cint(x), self.display.graphics_y + self.cint(y)) if hasattr(self.display, 'test') else 0,
            "REMAIN": self.do_remain,
            "INKEY": lambda key: self.display.get_inkey_state(self.cint(key)),
            "COPYCHR_STR": lambda stream=0: self.display.copychr(self.cint(stream)) if hasattr(self.display, 'copychr') else "",
            "CREAL": float,
            "CINT": self.cint,
            "CPC_IDIV": self.cpc_idiv,
            "CPC_MOD": self.cpc_mod,
            "ERR": lambda: self.err_code,
            "ERL": lambda: self.err_line,
            "DERR": lambda: 0,
            "FRE": lambda x=0: 40000,
            "INP": lambda x=0: 0,
            "FIX": int,
            "ROUND": lambda x, d=0: self.cpc_round(x, d) if d > 0 else int(self.cpc_round(x, d)),
            "UNT": lambda x: (self.cint(x) & 0xFFFF) - 65536 if (self.cint(x) & 0xFFFF) >= 32768 else (self.cint(x) & 0xFFFF),
            "LEFT_STR": lambda s, n: s[:self.cint(n)] if self.cint(n) > 0 else "",
            "UPPER_STR": lambda s: s.upper(),
            "STR_STR": lambda x: self.format_cpc_number(x, with_leading_space=True),
            "SPACE_STR": lambda n: " " * max(0, self.cint(n)),
            "STRING_STR": lambda n, c: (chr(self.cint(c) & 0xFF) if isinstance(c, (int, float)) else c[0]) * max(0, self.cint(n)),
            "HEX_STR": lambda x, w=None: hex(self.cint(x) & 0xFFFF)[2:].upper().zfill(self.cint(w)) if w else hex(self.cint(x) & 0xFFFF)[2:].upper(),
            "BIN_STR": lambda x, w=None: bin(self.cint(x) & 0xFFFF)[2:].zfill(self.cint(w)) if w else bin(self.cint(x) & 0xFFFF)[2:],
            "INSTR": lambda a, b, c=None: b.find(c, self.cint(a)-1) + 1 if c is not None else a.find(b) + 1,
            "PEEK": self.do_peek,
            "JOY": lambda joy_id: self.get_joy_state(self.cint(joy_id)),
            "ATN": self.builtin_atn,
            "SGN": lambda x: 1 if x > 0 else (-1 if x < 0 else 0),
            "MIN": min,
            "EXP": self.builtin_exp,
            "DEC_STR": lambda x, fmt: format_cpc_field(x, str(fmt)) if isinstance(fmt, str) else str(x),
            "SPC": lambda x: " " * (max(0, self.cint(x)) % (self.get_stream_width(0) or 256)),
            "TAB": lambda x: " " * max(0, ((max(1, self.cint(x)) - 1) % (self.get_stream_width(0) or 256)) + 1 - self.get_stream_pos(0)),
            "EOF": self.check_eof
        }

    def consume_time_us(self, us):
        if getattr(self, 'speed', 'unlimited') != 'real':
            return
        self.virtual_time_us += us
        self.frame_virtual_time_us += us
        if self.frame_virtual_time_us >= 20000:
            frames = int(self.frame_virtual_time_us // 20000)
            self.frame_virtual_time_us %= 20000
            self.sync_real_time(frames)

    def sync_real_time(self, frames=1):
        if hasattr(self, 'display'):
            self.display.process_events()
            self.display.update()
        if hasattr(self, 'sound'):
            self.sound.update_queues()

        now = time.perf_counter()
        if self.last_sync_real_time is None:
            self.last_sync_real_time = now
            self.last_sync_virt_us = self.virtual_time_us
            return

        target_elapsed = (self.virtual_time_us - self.last_sync_virt_us) / 1000000.0
        actual_elapsed = now - self.last_sync_real_time
        import os
        if not os.environ.get('CPC_TEST_NO_SLEEP'):
            delay = target_elapsed - actual_elapsed
            if delay > 0.001:
                time.sleep(delay)
            elif delay < -0.1:
                self.last_sync_real_time = time.perf_counter()
                self.last_sync_virt_us = self.virtual_time_us

    def get_cpc_time(self):
        if getattr(self, 'speed', 'unlimited') == 'real':
            ticks = int(self.virtual_time_us * 300 / 1000000.0)
        else:
            current_ms = pygame.time.get_ticks() if 'pygame' in sys.modules else 0
            ticks = int(current_ms * 0.3)
        return self.time_offset + ticks

    def set_cpc_time(self, val):
        current_ticks = self.get_cpc_time() - self.time_offset
        self.time_offset = self.cint(val) - current_ticks

    def builtin_sin(self, x):
        if getattr(self, 'speed', 'unlimited') == 'real':
            self.consume_time_us(11800)
        rad = math.radians(x) if self.angle_mode == 'DEG' else x
        return math.sin(rad)

    def builtin_cos(self, x):
        if getattr(self, 'speed', 'unlimited') == 'real':
            self.consume_time_us(11800)
        rad = math.radians(x) if self.angle_mode == 'DEG' else x
        return math.cos(rad)

    def builtin_tan(self, x):
        if getattr(self, 'speed', 'unlimited') == 'real':
            self.consume_time_us(18000)
        rad = math.radians(x) if self.angle_mode == 'DEG' else x
        return math.tan(rad)

    def builtin_atn(self, x):
        if getattr(self, 'speed', 'unlimited') == 'real':
            self.consume_time_us(16000)
        res = math.atan(x)
        return math.degrees(res) if self.angle_mode == 'DEG' else res

    def builtin_sqr(self, x):
        if getattr(self, 'speed', 'unlimited') == 'real':
            self.consume_time_us(12000)
        return math.sqrt(x)

    def builtin_log(self, x):
        if getattr(self, 'speed', 'unlimited') == 'real':
            self.consume_time_us(12000)
        return math.log(x)

    def builtin_log10(self, x):
        if getattr(self, 'speed', 'unlimited') == 'real':
            self.consume_time_us(13000)
        return math.log10(x)

    def builtin_exp(self, x):
        if getattr(self, 'speed', 'unlimited') == 'real':
            self.consume_time_us(15000)
        return math.exp(x)

    def get_expr_cost(self, expr):
        if isinstance(expr, Literal):
            return 150
        elif isinstance(expr, Variable):
            return 250
        elif isinstance(expr, RawExpression):
            if hasattr(expr, '_cost_us'):
                return expr._cost_us
            cost = 0
            tokens = expr.tokens
            for i, t in enumerate(tokens):
                if t.type == 'IDENTIFIER':
                    if i + 1 < len(tokens) and tokens[i+1].value == '(':
                        cost += 2200
                    else:
                        cost += 250
                elif t.type in ('NUMBER', 'HEX_NUMBER', 'BIN_NUMBER'):
                    cost += 150
                elif t.type == 'STRING':
                    cost += 200
                elif t.type == 'SYMBOL':
                    v = t.value
                    if v == '^':
                        cost += 18000
                    elif v == '*':
                        cost += 1400
                    elif v in ('/', '\\'):
                        cost += 2200
                    elif v in ('+', '-'):
                        cost += 250
                    elif v in ('=', '<>', '<', '>', '<=', '>='):
                        cost += 400
                elif t.type == 'KEYWORD':
                    kw = t.value.upper()
                    if kw in ('AND', 'OR', 'XOR', 'NOT'):
                        cost += 350
                    elif kw == 'MOD':
                        cost += 2200
            expr._cost_us = cost
            return cost
        return 150

    def get_statement_cost_us(self, stmt):
        st = type(stmt).__name__
        if st == 'PlotStatement':
            return 2360
        elif st == 'PlotrStatement':
            return 2760
        elif st == 'DrawStatement':
            return 3500
        elif st == 'DrawrStatement':
            return 3900
        elif st == 'PokeStatement':
            return 1530
        elif st == 'LetStatement':
            return 500
        elif st == 'LetArrayStatement':
            return 1500
        elif st == 'ForStatement':
            return 1200
        elif st == 'NextStatement':
            return 607
        elif st == 'LocateStatement':
            return 1300
        elif st == 'PrintStatement':
            return 1200
        elif st == 'ClsStatement':
            return 18000
        elif st == 'ClgStatement':
            return 20000
        elif st == 'ModeStatement':
            return 35000
        elif st == 'OriginStatement':
            return 800
        elif st in ('GosubStatement', 'ReturnStatement'):
            return 1000
        elif st == 'GotoStatement':
            return 600
        elif st == 'IfStatement':
            return 500
        elif st == 'DimStatement':
            return 1500
        elif st in ('EnvStatement', 'EntStatement', 'SoundStatement'):
            return 2500
        else:
            return 600

    def get_stream_pos(self, stream=0):
        s = self.cint(stream)
        if 0 <= s <= 7:
            if hasattr(self, 'display') and hasattr(self.display, 'get_pos'):
                return self.display.get_pos(s)
            return 1
        elif s == 8:
            return getattr(self, 'printer_pos', 1)
        elif s == 9:
            return getattr(self, 'file_out_pos', 1)
        return 1

    def get_stream_vpos(self, stream=0):
        s = self.cint(stream)
        if 0 <= s <= 7:
            if hasattr(self, 'display') and hasattr(self.display, 'get_vpos'):
                return self.display.get_vpos(s)
        return 1

    def get_stream_width(self, stream=0):
        s = self.cint(stream)
        if 0 <= s <= 7:
            if hasattr(self, 'display') and hasattr(self.display, 'get_text_window'):
                left, right, _, _ = self.display.get_text_window(s)
                return right - left + 1
            return 40
        elif s == 8:
            pw = getattr(self, 'printer_width', 132)
            return None if pw == 255 else pw
        return None

    def format_cpc_number(self, val, with_leading_space=True):
        if isinstance(val, bool):
            val = int(val)
        is_neg = val < 0
        abs_v = abs(val)
        if isinstance(abs_v, int) or (isinstance(abs_v, float) and abs_v.is_integer() and abs_v < 1e9):
            s = str(int(abs_v))
        else:
            s = f"{abs_v:.9g}".upper()
        if is_neg:
            return "-" + s
        elif with_leading_space:
            return " " + s
        return s

    def _count_printable_prefix(self, text):
        count = 0
        i = 0
        n = len(text)
        while i < n:
            code = ord(text[i])
            if code < 32:
                if code == 1:
                    count += 1
                    i += 2
                    continue
                break
            count += 1
            i += 1
        return count
        
    def cpc_rnd(self, x=None):
        if x is not None:
            if x < 0:
                random.seed(x)
                self.last_rnd = random.random()
            elif x == 0:
                if not hasattr(self, 'last_rnd'):
                    self.last_rnd = random.random()
                return self.last_rnd
            else:
                self.last_rnd = random.random()
        else:
            self.last_rnd = random.random()
        return self.last_rnd

    def cint(self, x):
        try:
            f = float(x)
            return int(math.copysign(math.floor(abs(f) + 0.5), f))
        except (ValueError, TypeError):
            return 0

    def cpc_round(self, x, d=0):
        m = 10 ** d
        val = x * m
        rounded = math.copysign(math.floor(abs(val) + 0.5), val)
        return rounded / m if d > 0 else int(rounded)

    def cpc_idiv(self, a, b):
        ia, ib = self.cint(a), self.cint(b)
        if ib == 0:
            raise ZeroDivisionError()
        return int(ia / ib)

    def cpc_mod(self, a, b):
        ia, ib = self.cint(a), self.cint(b)
        if ib == 0:
            raise ZeroDivisionError()
        return ia - int(ia / ib) * ib

    def do_remain(self, timer_id):
        t_id = self.cint(timer_id)
        t_info = self.timers.get(t_id)
        if t_info is not None:
            current_time = pygame.time.get_ticks() if 'pygame' in sys.modules else 0
            rem_ms = max(0, t_info['next_trigger'] - current_time)
            self.timers[t_id] = None
            return int(rem_ms // 20)
        return 0

    def check_eof(self):
        if not hasattr(self, 'file_in') or 9 not in self.file_in:
            return -1
        try:
            pos = self.file_in[9].tell()
            char = self.file_in[9].read(1)
            if not char:
                return -1
            self.file_in[9].seek(pos)
            return 0
        except:
            return -1

    def init_font_ram(self):
        from video.font_rom import CPC_FONT
        for c in range(256):
            matrix = CPC_FONT.get(c, [0]*8)
            for idx, b in enumerate(matrix):
                ram_addr = 42597 + c * 8 + idx
                if ram_addr < len(self.ram):
                    self.ram[ram_addr] = b

    def do_peek(self, addr):
        addr = int(addr) & 0xFFFF
        if addr >= 0xC000:
            return self.display.peek_video_ram(addr)
        return self.ram[addr]

    def fw_km_reset(self):
        if hasattr(self, 'display') and hasattr(self.display, 'key_buffer'):
            self.display.key_buffer.clear()

    def fw_km_wait_char(self):
        while True:
            if getattr(self.display, 'quit_requested', False):
                self.running = False
                return
            self.display.process_events()
            self.display.update()
            if self.display.key_buffer:
                char = self.display.key_buffer.pop(0)
                self.z80.A = ord(char)
                break
            pygame.time.wait(10)

    def fw_txt_output(self):
        char = chr(self.z80.A)
        self.display.print_text(char)

    def fw_txt_rd_char(self):
        if hasattr(self, 'display') and hasattr(self.display, 'copychr'):
            ch = self.display.copychr(0)
            self.z80.A = ord(ch[0]) if ch else 32
            self.z80.F |= 1
        else:
            self.z80.A = 32
            self.z80.F |= 1

    def fw_txt_set_cursor(self):
        self.display.locate(self.z80.H, self.z80.L)
        
    def fw_txt_get_cursor(self):
        self.z80.H = getattr(self.display, 'text_col', 1)  # Or stream handling... wait, text_col is in streams[0]
        # Actually in display.py: self.streams[stream]['text_col']
        self.z80.H = self.display.streams[0]['text_col'] if hasattr(self.display, 'streams') else 1
        self.z80.L = self.display.streams[0]['text_row'] if hasattr(self.display, 'streams') else 1
        
    def fw_txt_set_pen(self):
        self.display.set_pen(self.z80.A)
        
    def fw_txt_set_paper(self):
        self.display.set_paper(self.z80.A)
        
    def _to_signed16(self, val):
        return val - 65536 if val >= 32768 else val
        
    def fw_gra_move_absolute(self):
        x = self._to_signed16(self.z80.DE)
        y = self._to_signed16(self.z80.HL)
        self.display.move(x, y)
        
    def fw_gra_line_absolute(self):
        x = self._to_signed16(self.z80.DE)
        y = self._to_signed16(self.z80.HL)
        self.display.draw(x, y)
        
    def fw_gra_set_pen(self):
        self.display.set_graphics_pen(self.z80.A)
        
    def fw_scr_set_mode(self):
        self.display.set_mode(self.z80.A)
        
    def fw_scr_get_mode(self):
        self.z80.A = self.display.mode
        
    def fw_scr_clear(self):
        self.display.clear_graphics_window()
        self.display.clear_graphics(0) # stream 0

    def fw_scr_set_offset(self):
        # &BC05: SCR SET OFFSET (HL = screen base/offset)
        pass

    def fw_scr_access(self):
        # &BC59: GRA SET WRITE MODE (A = write mode: 0=normal, 1=XOR, 2=AND, 3=OR)
        if hasattr(self, 'display') and hasattr(self.display, 'set_graphics_write_mode'):
            self.display.set_graphics_write_mode(self.z80.A % 4)

    def fw_scr_set_ink(self):
        self.display.set_ink(self.z80.A, self.z80.B, self.z80.C)
        
    def fw_scr_set_border(self):
        self.display.set_border(self.z80.B, self.z80.C)

    def fw_km_get_joystick(self):
        self.display.process_events()
        joy0 = self.get_joy_state(0)
        joy1 = self.get_joy_state(1)
        self.z80.A = joy0
        self.z80.H = joy0
        self.z80.L = joy1
        
    def function_sq(self, channel_arg):
        """Función BASIC SQ(channel): devuelve estado de la cola y desarma eventos ON SQ."""
        ch = self.cint(channel_arg)
        if ch not in (1, 2, 4):
            self.trigger_error(5, self.pc)
        return self.sound.get_sq_status(ch, disarm=True)

    def fw_sound_reset(self):
        """SOUND RESET (&BCA7): Silencia todos los canales y limpia las colas."""
        self.sound.reset()
        self.sq_targets = {0: 0, 1: 0, 2: 0}
        if hasattr(self, 'sq_timers'):
            self.sq_timers.clear()

    def fw_sound_queue(self):
        """SOUND QUEUE (&BCAA): Añade un sonido a la cola desde el bloque en HL."""
        addr = self.z80.HL
        if addr + 8 > 65535:
            self.z80.F &= ~1  # Carry clear (fallo)
            return
            
        status = self.ram[addr]
        env = self.ram[addr+1]
        ent = self.ram[addr+2]
        period = self.ram[addr+3] | (self.ram[addr+4] << 8)
        noise = self.ram[addr+5]
        volume = self.ram[addr+6]
        duration = self.ram[addr+7] | (self.ram[addr+8] << 8)
        
        # Convertir duración a entero con signo de 16 bits
        duration = self._to_signed16(duration)
        
        ok = self.sound.play_sound(status, period, duration, volume, env, ent, noise, blocking=False)
        if ok:
            self.z80.F |= 1   # Carry true
        else:
            self.z80.F &= ~1  # Carry false

    def fw_sound_check(self):
        """SOUND CHECK (&BCAD): Comprueba el estado de la cola del canal indicado en A."""
        chan_mask = self.z80.A
        status = self.sound.get_sq_status(chan_mask, disarm=True)
        self.z80.A = status

    def fw_sound_arm_event(self):
        """SOUND ARM EVENT (&BCB0): Arma evento cuando hay espacio en la cola del canal en A."""
        chan_mask = self.z80.A
        self.sound.arm_sq_event(chan_mask)
        return self.sound.get_sq_status(chan_mask, disarm=False)

    def fw_sound_release(self):
        """SOUND RELEASE (&BCB3): Libera canales en Hold según máscara de canales en A."""
        channels = self.z80.A
        self.sound.release_channels(channels)

    def fw_sound_hold(self):
        """SOUND HOLD (&BCB6): Pausa todos los canales activos del PSG."""
        held = self.sound.hold_all()
        if held:
            self.z80.F |= 1
        else:
            self.z80.F &= ~1

    def fw_sound_continue(self):
        """SOUND CONTINUE (&BCB9): Reanuda todos los canales tras SOUND HOLD."""
        self.sound.continue_all()

    def fw_sound_ampl_envelope(self):
        """SOUND AMPL ENVELOPE (&BCBC): Define envolvente de volumen desde bloque en HL."""
        env_no = self.z80.A
        addr = self.z80.HL
        if 1 <= env_no <= 15 and addr + 16 <= 65536:
            block = bytes(self.ram[addr:addr+16])
            self.sound.set_env_from_ram(env_no, block)
            dest = 0xB2A6 + 16 * env_no
            self.ram[dest:dest+16] = block
            self.z80.HL = (addr + 16) & 0xFFFF
            self.z80.F |= 1
        else:
            self.z80.F &= ~1

    def fw_sound_tone_envelope(self):
        """SOUND TONE ENVELOPE (&BCBF): Define envolvente de tono desde bloque en HL."""
        ent_no = self.z80.A
        addr = self.z80.HL
        if 1 <= ent_no <= 15 and addr + 16 <= 65536:
            block = bytes(self.ram[addr:addr+16])
            self.sound.set_ent_from_ram(ent_no, block)
            dest = 0xB396 + 16 * ent_no
            self.ram[dest:dest+16] = block
            self.z80.HL = (addr + 16) & 0xFFFF
            self.z80.F |= 1
        else:
            self.z80.F &= ~1

    def fw_sound_a_address(self):
        """SOUND A ADDRESS (&BCC2): Devuelve en HL la dirección de la envolvente de amplitud A y BC=16."""
        env_no = self.z80.A
        if 1 <= env_no <= 15:
            self.z80.HL = 0xB2A6 + 16 * env_no
            self.z80.BC = 16
            self.z80.F |= 1
        else:
            self.z80.F &= ~1

    def fw_sound_t_address(self):
        """SOUND T ADDRESS (&BCC5): Devuelve en HL la dirección de la envolvente de tono A y BC=16."""
        ent_no = self.z80.A
        if 1 <= ent_no <= 15:
            self.z80.HL = 0xB396 + 16 * ent_no
            self.z80.BC = 16
            self.z80.F |= 1
        else:
            self.z80.F &= ~1

    def fw_mc_sound_register(self):
        """MC SOUND REGISTER (&BD34): Escribe el valor C en el registro A del AY-3-8912."""
        self.sound.write_psg_register(self.z80.A, self.z80.C)

    def _sync_env_ram(self, env_no):
        """Sincroniza la envolvente de volumen env_no en el área de RAM del firmware (&ADA2 y &B2A6+16*N)."""
        if not (1 <= env_no <= 15):
            return
        grouped = self.sound.envelopes_vol.get(env_no, [])
        block = bytearray(16)
        block[0] = len(grouped) & 0x7F
        for i, sec in enumerate(grouped[:5]):
            base = 1 + i * 3
            s0, s1, s2 = int(sec[0]), int(sec[1]), int(sec[2])
            if s0 == -1:
                block[base] = 0x80 | (s1 & 0x0F)
                block[base + 1] = s2 & 0xFF
                block[base + 2] = (s2 >> 8) & 0xFF
            else:
                block[base] = s0 & 0x7F
                block[base + 1] = s1 & 0xFF
                block[base + 2] = s2 & 0xFF
        self.ram[0xADA2:0xADB2] = block
        dest = 0xB2A6 + 16 * env_no
        self.ram[dest:dest + 16] = block

    def _sync_ent_ram(self, ent_no):
        """Sincroniza la envolvente de tono ent_no en el área de RAM del firmware (&ADA2 y &B396+16*N)."""
        actual_no = abs(int(ent_no))
        if not (1 <= actual_no <= 15):
            return
        ent_data = self.sound.envelopes_tone.get(actual_no, {})
        grouped = ent_data.get('sections', []) if isinstance(ent_data, dict) else ent_data
        repeat = ent_data.get('repeat', False) if isinstance(ent_data, dict) else (ent_no < 0)
        block = bytearray(16)
        block[0] = (len(grouped) & 0x7F) | (0x80 if repeat else 0)
        for i, sec in enumerate(grouped[:5]):
            base = 1 + i * 3
            s0, s1, s2 = int(sec[0]), int(sec[1]), int(sec[2])
            if s0 == -1:
                block[base] = 0xF0 + ((s1 >> 8) & 0x0F)
                block[base + 1] = s1 & 0xFF
                block[base + 2] = s2 & 0xFF
            else:
                block[base] = s0 & 0xFF
                block[base + 1] = s1 & 0xFF
                block[base + 2] = s2 & 0xFF
        self.ram[0xADA2:0xADB2] = block
        dest = 0xB396 + 16 * actual_no
        self.ram[dest:dest + 16] = block

    def _has_pending_interrupt(self):
        if hasattr(self, 'display') and getattr(self.display, 'esc_pressed', False):
            return True
        if not self.interrupts_enabled:
            return False
        for c_id in range(3):
            if self.sound.sq_events_pending.get(c_id, False) and self.sq_targets.get(c_id, 0) > 0:
                return True
        current_time = pygame.time.get_ticks() if 'pygame' in sys.modules else 0
        for t_id in range(4):
            t_info = self.timers.get(t_id)
            if t_info and current_time >= t_info['next_trigger']:
                return True
        return False
        
    def fw_mc_wait_flyback(self):
        current_time = pygame.time.get_ticks()
        if not hasattr(self, 'last_flyback'):
            self.last_flyback = current_time
            
        wait_time = 20 - (current_time - self.last_flyback)
        if wait_time > 0:
            pygame.time.wait(wait_time)
            
        self.display.update()
        self.last_flyback = pygame.time.get_ticks()

    def fw_mc_set_mode(self):
        mode = getattr(self.z80, 'A', 0)
        self.display.set_hardware_mode(mode)

    def execute_machine_code(self, start_addr):
        pc = start_addr & 0xFFFF
        max_instructions = 100000
        call_stack = []
        instructions_run = 0

        def get_reg8(idx):
            if idx == 0: return self.z80.B
            elif idx == 1: return self.z80.C
            elif idx == 2: return self.z80.D
            elif idx == 3: return self.z80.E
            elif idx == 4: return self.z80.H
            elif idx == 5: return self.z80.L
            elif idx == 6: return self.ram[self.z80.HL]
            elif idx == 7: return self.z80.A
            return 0

        def set_reg8(idx, val):
            val &= 0xFF
            if idx == 0: self.z80.B = val
            elif idx == 1: self.z80.C = val
            elif idx == 2: self.z80.D = val
            elif idx == 3: self.z80.E = val
            elif idx == 4: self.z80.H = val
            elif idx == 5: self.z80.L = val
            elif idx == 6: self.ram[self.z80.HL] = val
            elif idx == 7: self.z80.A = val

        def get_reg16(idx):
            if idx == 0: return self.z80.BC
            elif idx == 1: return self.z80.DE
            elif idx == 2: return self.z80.HL
            elif idx == 3: return self.z80.SP
            return 0

        def set_reg16(idx, val):
            val &= 0xFFFF
            if idx == 0: self.z80.BC = val
            elif idx == 1: self.z80.DE = val
            elif idx == 2: self.z80.HL = val
            elif idx == 3: self.z80.SP = val

        def check_cc(cc):
            # 0: NZ, 1: Z, 2: NC, 3: C
            z = bool(self.z80.F & 0x40)
            c = bool(self.z80.F & 0x01)
            if cc == 0: return not z
            elif cc == 1: return z
            elif cc == 2: return not c
            elif cc == 3: return c
            return False

        def alu_op(op, val):
            val &= 0xFF
            a = self.z80.A
            if op == 0:  # ADD
                res = a + val
                self.z80.A = res & 0xFF
                self.z80.F = (0x01 if res > 0xFF else 0) | (0x40 if (res & 0xFF) == 0 else 0)
            elif op == 1:  # ADC
                carry = 1 if (self.z80.F & 0x01) else 0
                res = a + val + carry
                self.z80.A = res & 0xFF
                self.z80.F = (0x01 if res > 0xFF else 0) | (0x40 if (res & 0xFF) == 0 else 0)
            elif op == 2:  # SUB
                res = a - val
                self.z80.A = res & 0xFF
                self.z80.F = 0x02 | (0x01 if res < 0 else 0) | (0x40 if (res & 0xFF) == 0 else 0)
            elif op == 3:  # SBC
                carry = 1 if (self.z80.F & 0x01) else 0
                res = a - val - carry
                self.z80.A = res & 0xFF
                self.z80.F = 0x02 | (0x01 if res < 0 else 0) | (0x40 if (res & 0xFF) == 0 else 0)
            elif op == 4:  # AND
                res = a & val
                self.z80.A = res & 0xFF
                self.z80.F = 0x10 | (0x40 if (res & 0xFF) == 0 else 0)
            elif op == 5:  # XOR
                res = a ^ val
                self.z80.A = res & 0xFF
                self.z80.F = 0x40 if (res & 0xFF) == 0 else 0
            elif op == 6:  # OR
                res = a | val
                self.z80.A = res & 0xFF
                self.z80.F = 0x40 if (res & 0xFF) == 0 else 0
            elif op == 7:  # CP
                res = a - val
                self.z80.F = 0x02 | (0x01 if res < 0 else 0) | (0x40 if (res & 0xFF) == 0 else 0)

        while instructions_run < max_instructions:
            if pc in self.firmware_hooks:
                self.firmware_hooks[pc]()
                if call_stack:
                    pc = call_stack.pop()
                    continue
                else:
                    return True

            opcode = self.ram[pc]
            instructions_run += 1

            if opcode == 0x00:  # NOP
                pc = (pc + 1) & 0xFFFF

            elif opcode == 0xCD:  # CALL nn
                target = self.ram[(pc + 1) & 0xFFFF] | (self.ram[(pc + 2) & 0xFFFF] << 8)
                ret_addr = (pc + 3) & 0xFFFF
                if target in self.firmware_hooks:
                    self.firmware_hooks[target]()
                    pc = ret_addr
                else:
                    call_stack.append(ret_addr)
                    pc = target

            elif (opcode & 0xC7) == 0xC4:  # CALL cc, nn
                cc = (opcode >> 3) & 0x07
                target = self.ram[(pc + 1) & 0xFFFF] | (self.ram[(pc + 2) & 0xFFFF] << 8)
                ret_addr = (pc + 3) & 0xFFFF
                if check_cc(cc):
                    if target in self.firmware_hooks:
                        self.firmware_hooks[target]()
                        pc = ret_addr
                    else:
                        call_stack.append(ret_addr)
                        pc = target
                else:
                    pc = ret_addr

            elif opcode == 0xC3:  # JP nn
                target = self.ram[(pc + 1) & 0xFFFF] | (self.ram[(pc + 2) & 0xFFFF] << 8)
                if target in self.firmware_hooks:
                    self.firmware_hooks[target]()
                    if call_stack:
                        pc = call_stack.pop()
                    else:
                        return True
                else:
                    pc = target

            elif (opcode & 0xC7) == 0xC2:  # JP cc, nn
                cc = (opcode >> 3) & 0x07
                target = self.ram[(pc + 1) & 0xFFFF] | (self.ram[(pc + 2) & 0xFFFF] << 8)
                if check_cc(cc):
                    if target in self.firmware_hooks:
                        self.firmware_hooks[target]()
                        if call_stack:
                            pc = call_stack.pop()
                        else:
                            return True
                    else:
                        pc = target
                else:
                    pc = (pc + 3) & 0xFFFF

            elif opcode == 0x18:  # JR e
                offset = self.ram[(pc + 1) & 0xFFFF]
                if offset >= 128: offset -= 256
                pc = (pc + 2 + offset) & 0xFFFF

            elif (opcode & 0xE7) == 0x20:  # JR cc, e (NZ, Z, NC, C)
                cc = (opcode >> 3) & 0x03
                offset = self.ram[(pc + 1) & 0xFFFF]
                if offset >= 128: offset -= 256
                if check_cc(cc):
                    pc = (pc + 2 + offset) & 0xFFFF
                else:
                    pc = (pc + 2) & 0xFFFF

            elif opcode == 0x10:  # DJNZ e
                offset = self.ram[(pc + 1) & 0xFFFF]
                if offset >= 128: offset -= 256
                self.z80.B = (self.z80.B - 1) & 0xFF
                if self.z80.B != 0:
                    pc = (pc + 2 + offset) & 0xFFFF
                else:
                    pc = (pc + 2) & 0xFFFF

            elif opcode == 0xC9:  # RET
                if call_stack:
                    pc = call_stack.pop()
                else:
                    return True

            elif (opcode & 0xC7) == 0xC0:  # RET cc
                cc = (opcode >> 3) & 0x07
                if check_cc(cc):
                    if call_stack:
                        pc = call_stack.pop()
                    else:
                        return True
                else:
                    pc = (pc + 1) & 0xFFFF

            elif opcode == 0x32:  # LD (nn), A
                target = self.ram[(pc + 1) & 0xFFFF] | (self.ram[(pc + 2) & 0xFFFF] << 8)
                self.ram[target] = self.z80.A & 0xFF
                pc = (pc + 3) & 0xFFFF

            elif opcode == 0x3A:  # LD A, (nn)
                target = self.ram[(pc + 1) & 0xFFFF] | (self.ram[(pc + 2) & 0xFFFF] << 8)
                self.z80.A = self.ram[target]
                pc = (pc + 3) & 0xFFFF

            elif (opcode & 0xCF) == 0x01:  # LD rr, nn
                r_idx = (opcode >> 4) & 0x03
                val = self.ram[(pc + 1) & 0xFFFF] | (self.ram[(pc + 2) & 0xFFFF] << 8)
                set_reg16(r_idx, val)
                pc = (pc + 3) & 0xFFFF

            elif (opcode & 0xC7) == 0x06:  # LD r, n
                r_idx = (opcode >> 3) & 0x07
                val = self.ram[(pc + 1) & 0xFFFF]
                set_reg8(r_idx, val)
                pc = (pc + 2) & 0xFFFF

            elif 0x40 <= opcode <= 0x7F:
                if opcode == 0x76:  # HALT
                    return True
                dest = (opcode >> 3) & 0x07
                src = opcode & 0x07
                set_reg8(dest, get_reg8(src))
                pc = (pc + 1) & 0xFFFF

            elif 0x80 <= opcode <= 0xBF:  # ALU A, r
                op = (opcode >> 3) & 0x07
                src = opcode & 0x07
                alu_op(op, get_reg8(src))
                pc = (pc + 1) & 0xFFFF

            elif (opcode & 0xC7) == 0xC6:  # ALU A, n
                op = (opcode >> 3) & 0x07
                val = self.ram[(pc + 1) & 0xFFFF]
                alu_op(op, val)
                pc = (pc + 2) & 0xFFFF

            elif (opcode & 0xC7) == 0x04:  # INC r
                r_idx = (opcode >> 3) & 0x07
                val = (get_reg8(r_idx) + 1) & 0xFF
                set_reg8(r_idx, val)
                self.z80.F = (self.z80.F & 0x01) | (0x40 if val == 0 else 0)
                pc = (pc + 1) & 0xFFFF

            elif (opcode & 0xC7) == 0x05:  # DEC r
                r_idx = (opcode >> 3) & 0x07
                val = (get_reg8(r_idx) - 1) & 0xFF
                set_reg8(r_idx, val)
                self.z80.F = (self.z80.F & 0x01) | 0x02 | (0x40 if val == 0 else 0)
                pc = (pc + 1) & 0xFFFF

            elif (opcode & 0xCF) == 0x03:  # INC rr
                r_idx = (opcode >> 4) & 0x03
                set_reg16(r_idx, (get_reg16(r_idx) + 1) & 0xFFFF)
                pc = (pc + 1) & 0xFFFF

            elif (opcode & 0xCF) == 0x0B:  # DEC rr
                r_idx = (opcode >> 4) & 0x03
                set_reg16(r_idx, (get_reg16(r_idx) - 1) & 0xFFFF)
                pc = (pc + 1) & 0xFFFF

            elif opcode == 0xEB:  # EX DE, HL
                self.z80.DE, self.z80.HL = self.z80.HL, self.z80.DE
                pc = (pc + 1) & 0xFFFF

            elif (opcode & 0xCF) == 0xC5:  # PUSH rr (BC, DE, HL, AF)
                r_idx = (opcode >> 4) & 0x03
                val = self.z80.AF if r_idx == 3 else get_reg16(r_idx)
                self.z80.SP = (self.z80.SP - 2) & 0xFFFF
                self.ram[self.z80.SP] = val & 0xFF
                self.ram[(self.z80.SP + 1) & 0xFFFF] = (val >> 8) & 0xFF
                pc = (pc + 1) & 0xFFFF

            elif (opcode & 0xCF) == 0xC1:  # POP rr (BC, DE, HL, AF)
                r_idx = (opcode >> 4) & 0x03
                val = self.ram[self.z80.SP] | (self.ram[(self.z80.SP + 1) & 0xFFFF] << 8)
                self.z80.SP = (self.z80.SP + 2) & 0xFFFF
                if r_idx == 3:
                    self.z80.AF = val
                else:
                    set_reg16(r_idx, val)
                pc = (pc + 1) & 0xFFFF

            else:
                return False

        return False

    def get_joy_state(self, joy_id):
        keys = pygame.key.get_pressed()
        state = 0
        if joy_id == 0:
            if keys[pygame.K_UP]: state |= 1
            if keys[pygame.K_DOWN]: state |= 2
            if keys[pygame.K_LEFT]: state |= 4
            if keys[pygame.K_RIGHT]: state |= 8
            if keys[pygame.K_SPACE] or keys[pygame.K_z]: state |= 16
            if keys[pygame.K_x]: state |= 32
        elif joy_id == 1:
            if keys[pygame.K_w]: state |= 1
            if keys[pygame.K_s]: state |= 2
            if keys[pygame.K_a]: state |= 4
            if keys[pygame.K_d]: state |= 8
            if keys[pygame.K_LCTRL]: state |= 16
            if keys[pygame.K_LALT]: state |= 32
        return state

    def get_next_line(self, current_line):
        try:
            idx = self.line_numbers.index(current_line)
            if idx + 1 < len(self.line_numbers):
                return self.line_numbers[idx + 1]
        except ValueError:
            pass
        return None

    def _find_matching_next(self, target_var, curr_pc, curr_statements, stmt_idx):
        open_stack = [target_var]
        
        # 1. Search remaining statements on current line
        for idx in range(stmt_idx, len(curr_statements)):
            s = curr_statements[idx]
            if isinstance(s, ForStatement):
                open_stack.append(s.identifier)
            elif isinstance(s, NextStatement):
                ids = getattr(s, 'identifiers', [s.identifier])
                if not ids or ids == [None]:
                    if open_stack:
                        open_stack.pop()
                    if not open_stack:
                        return (curr_pc, idx + 1)
                else:
                    for v in ids:
                        if v in open_stack:
                            while open_stack and open_stack[-1] != v:
                                open_stack.pop()
                            if open_stack:
                                open_stack.pop()
                            if not open_stack:
                                return (curr_pc, idx + 1)

        # 2. Search subsequent lines
        try:
            start_l_idx = self.line_numbers.index(curr_pc) + 1
        except ValueError:
            return None
            
        for l_idx in range(start_l_idx, len(self.line_numbers)):
            pc = self.line_numbers[l_idx]
            line_stmts = self.program.lines[pc]
            for idx, s in enumerate(line_stmts):
                if isinstance(s, ForStatement):
                    open_stack.append(s.identifier)
                elif isinstance(s, NextStatement):
                    ids = getattr(s, 'identifiers', [s.identifier])
                    if not ids or ids == [None]:
                        if open_stack:
                            open_stack.pop()
                        if not open_stack:
                            return (pc, idx + 1)
                    else:
                        for v in ids:
                            if v in open_stack:
                                while open_stack and open_stack[-1] != v:
                                    open_stack.pop()
                                if open_stack:
                                    open_stack.pop()
                                if not open_stack:
                                    return (pc, idx + 1)
        return None

    def trigger_error(self, code, line_num):
        self.err_code = code
        self.err_line = line_num
        raise BasicErrorInterrupt()

    def typecast(self, var_name, val):
        if var_name.endswith('%'):
            return self.cint(val)
        elif var_name.endswith('!'):
            try: return float(val)
            except: return 0.0
        elif var_name.endswith('$'):
            return str(val)
        else:
            def_type = self.default_types.get(var_name[0].upper(), 'REAL')
            if def_type == 'INT':
                return self.cint(val)
            elif def_type == 'STR':
                return str(val)
            else:
                try: return float(val)
                except: return 0.0

    def get_default_value(self, var_name):
        if var_name.endswith('%'): return 0
        elif var_name.endswith('!'): return 0.0
        elif var_name.endswith('$'): return ""
        else:
            def_type = self.default_types.get(var_name[0].upper(), 'REAL')
            if def_type == 'INT': return 0
            elif def_type == 'STR': return ""
            else: return 0.0

    def evaluate(self, expr):
        if getattr(self, 'speed', 'unlimited') == 'real':
            self.consume_time_us(self.get_expr_cost(expr))
        if isinstance(expr, Literal):
            if expr.type == 'NUMBER':
                # very basic float/int distinction
                if '.' in expr.value:
                    return float(expr.value)
                return int(expr.value)
            elif expr.type == 'STRING':
                return expr.value
            elif expr.type == 'HEX_NUMBER':
                val = expr.value[1:].upper()
                if val.startswith('H'): val = val[1:]
                return int(val, 16)
            elif expr.type == 'BIN_NUMBER':
                return int(expr.value[2:], 2)
        elif isinstance(expr, RawExpression):
            if hasattr(expr, '_cached_code'):
                code_obj = expr._cached_code
            else:
                s = ""
                skip_next = False
                for i, t in enumerate(expr.tokens):
                    if skip_next:
                        skip_next = False
                        continue
                    if t.type == 'IDENTIFIER':
                        val_upper = t.value.upper()
                        if val_upper == 'FN' and i + 1 < len(expr.tokens) and expr.tokens[i+1].type == 'IDENTIFIER':
                            val_upper = "FN" + expr.tokens[i+1].value.upper()
                            skip_next = True
                        
                        if val_upper == 'INKEY$':
                            s += "GET_INKEY_STR()"
                        elif val_upper in ('CHR$', 'LEFT$', 'RIGHT$', 'MID$', 'STR$', 'SPACE$', 'COPYCHR$', 'UPPER$', 'LOWER$', 'STRING$', 'HEX$', 'BIN$', 'DEC$'):
                            s += val_upper.replace('$', '_STR')
                        elif val_upper in self.builtins:
                            kw = val_upper
                            s += kw
                            if kw in ("RND", "TIME", "XPOS", "YPOS", "VPOS", "POS", "INKEY", "ERR", "ERL", "DERR", "FRE", "INP", "HIMEM"):
                                next_idx = i + 2 if skip_next else i + 1
                                if next_idx >= len(expr.tokens) or expr.tokens[next_idx].value != '(':
                                    s += "()"
                        elif skip_next or val_upper in self.user_functions:
                            safe_fn = val_upper.replace('%', '_PCT').replace('$', '_DLR').replace('!', '_EXC').replace('.', '_DOT_')
                            s += f"USER_FN_{safe_fn}"
                            # If called without parenthesis, add them
                            next_idx = i + 2 if skip_next else i + 1
                            if next_idx >= len(expr.tokens) or expr.tokens[next_idx].value != '(':
                                s += "()"
                        elif (i + 2 if skip_next else i + 1) < len(expr.tokens) and expr.tokens[(i + 2 if skip_next else i + 1)].value == '(':
                            if t.value not in self.arrays:
                                self.arrays[t.value] = {}
                            s += t.value.replace('%', '_PCT').replace('$', '_DLR').replace('!', '_EXC').replace('.', '_DOT_')
                        else:
                            s += f"GET_VAR({repr(t.value)})"
                    elif t.type == 'HEX_NUMBER':
                        val = t.value[1:].upper()
                        if val.startswith('H'): val = val[1:]
                        s += "0x" + val
                    elif t.type == 'BIN_NUMBER':
                        s += "0b" + t.value[2:]
                    elif t.type == 'SYMBOL' and t.value == '=':
                        s += '=='
                    elif t.type == 'SYMBOL' and t.value == '<>':
                        s += '!='
                    elif t.type == 'SYMBOL' and t.value == '^':
                        s += '**'
                    elif t.type == 'SYMBOL' and t.value == '\\':
                        s += '//'
                    elif t.type == 'SYMBOL' and t.value == '#':
                        pass  # ignore stream symbol
                    elif t.type == 'KEYWORD':
                        kw = t.value.upper()
                        if kw == 'MOD': s += ' % '
                        elif kw == 'AND': s += ' and '
                        elif kw == 'OR': s += ' or '
                        elif kw == 'NOT': s += ' not '
                        elif kw == 'XOR': s += ' ^ '
                        elif kw in self.builtins:
                            s += kw
                            if kw in ("RND", "TIME", "XPOS", "YPOS", "VPOS", "POS", "INKEY", "JOY", "PEEK", "LEN", "ERR", "ERL", "EOF", "DERR", "FRE", "INP", "HIMEM"):
                                if i + 1 >= len(expr.tokens) or expr.tokens[i+1].value != '(':
                                    s += "()"
                        elif (i + 1) < len(expr.tokens) and expr.tokens[i + 1].value == '(':
                            if kw not in self.arrays:
                                self.arrays[kw] = {}
                            s += kw.replace('%', '_PCT').replace('$', '_DLR').replace('!', '_EXC').replace('.', '_DOT_')
                        else:
                            s += f"GET_VAR({repr(kw)})"
                    elif t.type == 'STRING':
                        s += repr(t.value)
                    else:
                        s += str(t.value)
                        
                open_parens = sum(1 for t in expr.tokens if t.type == 'SYMBOL' and t.value == '(')
                close_parens = sum(1 for t in expr.tokens if t.type == 'SYMBOL' and t.value == ')')
                if open_parens > close_parens:
                    s += ')' * (open_parens - close_parens)
                    
                try:
                    class BitwiseTransformer(ast.NodeTransformer):
                        def visit_BoolOp(self, node):
                            self.generic_visit(node)
                            if isinstance(node.op, ast.And):
                                res = ast.Call(func=ast.Name(id='CINT', ctx=ast.Load()), args=[node.values[0]], keywords=[])
                                for val in node.values[1:]:
                                    v_int = ast.Call(func=ast.Name(id='CINT', ctx=ast.Load()), args=[val], keywords=[])
                                    res = ast.BinOp(left=res, op=ast.BitAnd(), right=v_int)
                                return ast.copy_location(res, node)
                            elif isinstance(node.op, ast.Or):
                                res = ast.Call(func=ast.Name(id='CINT', ctx=ast.Load()), args=[node.values[0]], keywords=[])
                                for val in node.values[1:]:
                                    v_int = ast.Call(func=ast.Name(id='CINT', ctx=ast.Load()), args=[val], keywords=[])
                                    res = ast.BinOp(left=res, op=ast.BitOr(), right=v_int)
                                return ast.copy_location(res, node)
                            return node
                        def visit_UnaryOp(self, node):
                            self.generic_visit(node)
                            if isinstance(node.op, ast.Not):
                                v_int = ast.Call(func=ast.Name(id='CINT', ctx=ast.Load()), args=[node.operand], keywords=[])
                                return ast.copy_location(ast.UnaryOp(op=ast.Invert(), operand=v_int), node)
                            return node
                        def visit_Compare(self, node):
                            self.generic_visit(node)
                            return ast.copy_location(ast.UnaryOp(op=ast.USub(), operand=node), node)
                        def visit_BinOp(self, node):
                            self.generic_visit(node)
                            if isinstance(node.op, ast.BitXor):
                                node.left = ast.Call(func=ast.Name(id='CINT', ctx=ast.Load()), args=[node.left], keywords=[])
                                node.right = ast.Call(func=ast.Name(id='CINT', ctx=ast.Load()), args=[node.right], keywords=[])
                            elif isinstance(node.op, ast.FloorDiv):
                                return ast.copy_location(ast.Call(func=ast.Name(id='CPC_IDIV', ctx=ast.Load()), args=[node.left, node.right], keywords=[]), node)
                            elif isinstance(node.op, ast.Mod):
                                return ast.copy_location(ast.Call(func=ast.Name(id='CPC_MOD', ctx=ast.Load()), args=[node.left, node.right], keywords=[]), node)
                            return node
                            
                    tree = ast.parse(s.lstrip(), mode='eval')
                    tree = BitwiseTransformer().visit(tree)
                    ast.fix_missing_locations(tree)
                    code_obj = compile(tree, '<basic_expr>', 'eval')
                    expr._cached_code = code_obj
                except Exception as e:
                    print(f"Error compiling '{s}': {e}")
                    return 0

            try:
                cint_fn = self.cint
                class ArrayWrapper:
                    def __init__(self, arr_dict, is_string):
                        self.arr_dict = arr_dict
                        self.is_string = is_string
                    def __call__(self, *args):
                        return self.arr_dict.get(tuple(cint_fn(a) for a in args), "" if self.is_string else 0)
                
                eval_globals = self.builtins.copy()
                def get_var_or_reg(name):
                    if name.startswith('_REG_'):
                        return getattr(self.z80, name[5:], 0)
                    return self.variables.get(name, self.get_default_value(name))
                eval_globals['GET_VAR'] = get_var_or_reg
                eval_globals['GET_INKEY_STR'] = lambda: self.display.get_inkey_str()
                
                for arr_name, arr_dict in self.arrays.items():
                    safe_name = arr_name.replace('%', '_PCT').replace('$', '_DLR').replace('!', '_EXC').replace('.', '_DOT_')
                    eval_globals[safe_name] = ArrayWrapper(arr_dict, arr_name.endswith('$'))
                for fn_name, fn_func in self.user_functions.items():
                    safe_fn = fn_name.replace('%', '_PCT').replace('$', '_DLR').replace('!', '_EXC').replace('.', '_DOT_')
                    eval_globals[f"USER_FN_{safe_fn}"] = fn_func
                    
                return eval(code_obj, eval_globals, {})
            except ZeroDivisionError:
                self.trigger_error(11, self.pc)
            except OverflowError:
                self.trigger_error(6, self.pc)
            except TypeError as e:
                import traceback
                traceback.print_exc()
                print("TYPE ERROR DETECTED:", e)
                if hasattr(expr, '_cached_code'):
                    import dis
                    print("DISASSEMBLY OF CACHED CODE:")
                    dis.dis(expr._cached_code)
                self.trigger_error(13, self.pc)
            except BasicErrorInterrupt:
                raise
            except Exception as e:
                # We can't print 's' here easily if code_obj was used, but we can just say error.
                print(f"Error evaluating expression: {e}")
                return 0

        return 0

    def collect_data(self):
        for line_num in self.line_numbers:
            for stmt in self.program.lines[line_num]:
                if isinstance(stmt, DataStatement):
                    for val in stmt.values:
                        self.data_values.append((line_num, val))

    def execute(self):
        if not self.line_numbers:
            return
            
        self.collect_data()
        self.pc = self.line_numbers[0]
        self.running = True
        self.virtual_time_us = 0
        self.frame_virtual_time_us = 0
        self.time_offset = 0
        self.last_sync_real_time = time.perf_counter()
        self.last_sync_virt_us = 0
        if hasattr(self, 'display'):
            import pygame
            if pygame.display.get_surface() is None:
                pygame.display.init()
                self.display.screen = pygame.display.set_mode((self.display.width * self.display.scale, self.display.height * self.display.scale))
                self.display.logical_surface.fill(self.display.current_paper)
                self.display.update()
            self.display.quit_requested = False
        
        self.stmts_this_frame = 0
        self.stmts_since_event = 0
        self.last_time = pygame.time.get_ticks() if 'pygame' in sys.modules else 0
        statements_limit = 37 # Approx. real CPC BASIC statements per 20ms frame (gives ~5.44s for 5000 empty FOR loops)
        
        while self.running and self.pc is not None:
            if getattr(self.display, 'quit_requested', False):
                self.running = False
                self.display.quit_requested = False
                break
            is_real_speed = getattr(self, 'speed', 'unlimited') == 'real'
            current_time = int(self.virtual_time_us // 1000) if is_real_speed else (pygame.time.get_ticks() if 'pygame' in sys.modules else 0)
            self.last_time = current_time

            # -- Keyboard Interrupt Check (ON BREAK) --
            if hasattr(self, 'display') and getattr(self.display, 'esc_pressed', False):
                self.display.esc_pressed = False
                action = getattr(self, 'on_break_action', 'CONT')
                if action == 'GOSUB' and hasattr(self, 'on_break_line'):
                    saved_restore = getattr(self, 'restore_statements', None)
                    if hasattr(self, 'restore_statements'):
                        del self.restore_statements
                    self.gosub_stack.append((self.pc, getattr(self, 'next_stmt_idx', 0), True, saved_restore))
                    self.next_stmt_idx = 0
                    self.pc = self.on_break_line
                    self.interrupts_enabled = False
                    continue
                elif action == 'STOP':
                    print(f"Break in line {self.pc}")
                    if hasattr(self, 'display'):
                        self.display.print(f"Break in line {self.pc}\r\n")
                    self.running = False
                    continue

            # -- Timer Interrupt Check (AFTER / EVERY / SQ) --
            interrupt_triggered = False
            self.sound.update_queues()
            if self.interrupts_enabled:
                for c_id in range(3):
                    if self.sound.sq_events_pending.get(c_id, False):
                        self.sound.sq_events_pending[c_id] = False
                        target = self.sq_targets.get(c_id, 0)
                        if target > 0 and target in self.program.lines:
                            saved_restore = getattr(self, 'restore_statements', None)
                            if hasattr(self, 'restore_statements'):
                                del self.restore_statements
                            self.gosub_stack.append((self.pc, getattr(self, 'next_stmt_idx', 0), True, saved_restore))
                            self.next_stmt_idx = 0
                            self.pc = target
                            self.interrupts_enabled = False
                            interrupt_triggered = True
                            break
                            
                if not interrupt_triggered:
                    for t_id in range(4):
                        t_info = self.timers.get(t_id)
                        if t_info and current_time >= t_info['next_trigger']:
                            # Trigger interrupt: save current PC and statement index, jump to target line
                            saved_restore = getattr(self, 'restore_statements', None)
                            if hasattr(self, 'restore_statements'):
                                del self.restore_statements
                            self.gosub_stack.append((self.pc, getattr(self, 'next_stmt_idx', 0), True, saved_restore))
                            self.next_stmt_idx = 0
                            self.pc = t_info['target']
                            self.interrupts_enabled = False # Implicit DI
                            if t_info['type'] == 'EVERY':
                                t_info['next_trigger'] = current_time + t_info['delay_ms']
                            else:
                                self.timers[t_id] = None
                            interrupt_triggered = True
                            break # Execute only one interrupt at a time
            
            if interrupt_triggered:
                continue
                
            if hasattr(self, 'restore_statements'):
                statements = self.restore_statements
                del self.restore_statements
            else:
                statements = list(self.program.lines.get(self.pc, []))
            next_pc = self.get_next_line(self.pc)
            
            stmt_idx = getattr(self, 'next_stmt_idx', 0)
            self.next_stmt_idx = 0
            try:
                while stmt_idx < len(statements):
                    self._current_stmt_idx = stmt_idx

                    stmt = statements[stmt_idx]
                    stmt_idx += 1
                    
                    self.stmts_since_event += 1
                    if self.stmts_since_event >= 80:
                        current_time = pygame.time.get_ticks() if 'pygame' in sys.modules else 0
                        self.last_time = current_time
                        if hasattr(self, 'display'):
                            self.display.process_events()
                            if getattr(self.display, 'quit_requested', False):
                                self.running = False
                                break
                            if current_time - getattr(self, 'last_update', 0) >= 20:
                                self.display.update()
                                self.last_update = current_time
                                self.stmts_this_frame = 0
                        self.stmts_since_event = 0

                    s_type = type(stmt).__name__
                    has_active_timer = any(t is not None for t in self.timers.values())
                    if is_real_speed:
                        self.consume_time_us(self.get_statement_cost_us(stmt))
                    elif has_active_timer and s_type in ('DrawStatement', 'DrawrStatement', 'PlotStatement', 'PlotrStatement'):
                        cost = 1
                        if s_type in ('DrawStatement', 'DrawrStatement', 'PlotStatement', 'PlotrStatement', 'ClsStatement', 'ClgStatement', 'FillStatement', 'SoundStatement'):
                            cost = 9
                        self.stmts_this_frame += cost
                        if self.stmts_this_frame >= statements_limit:
                            if hasattr(self, 'display'):
                                self.display.process_events()
                                self.display.update()
                            current_t = pygame.time.get_ticks() if 'pygame' in sys.modules else 0
                            wait_time = 20 - (current_t - getattr(self, 'last_update', 0))
                            if wait_time > 0 and 'pygame' in sys.modules:
                                pygame.time.wait(wait_time)
                            self.last_update = pygame.time.get_ticks() if 'pygame' in sys.modules else 0
                            self.last_time = self.last_update
                            self.stmts_this_frame = 0
                            self.stmts_since_event = 0
                    
                    if isinstance(stmt, PrintStatement):
                        stream = self.cint(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) is not None else 0
                        target_stream = 0 if stream == 8 else stream
                        out = []
                        newline = True
                        current_using_fmt = None
                        current_vals_for_using = []

                        def print_chunk(chunk):
                            if not chunk:
                                return
                            if stream == 8:
                                for ch in chunk:
                                    if ch in ('\r', '\n'):
                                        self.printer_pos = 1
                                    elif ord(ch) >= 32:
                                        self.printer_pos = getattr(self, 'printer_pos', 1) + 1
                            elif stream == 9:
                                for ch in chunk:
                                    if ch in ('\r', '\n'):
                                        self.file_out_pos = 1
                                    elif ord(ch) >= 32:
                                        self.file_out_pos = getattr(self, 'file_out_pos', 1) + 1
                            if stream != 9 and hasattr(self, 'display'):
                                self.display.print_text(chunk, target_stream)
                                if is_real_speed:
                                    mode = getattr(self.display, 'mode', 1)
                                    char_cost = 3300 if mode == 0 else (2800 if mode == 1 else 900)
                                    for ch in chunk:
                                        if ch in ('\r', '\n'):
                                            self.consume_time_us(600)
                                        else:
                                            self.consume_time_us(char_cost)

                        def poss_validate_xpos(required_chars):
                            w = self.get_stream_width(stream)
                            if w is not None and w > 0:
                                col = self.get_stream_pos(stream)
                                if col > 1 and (col - 1) + required_chars > w:
                                    out.append("\n")
                                    print_chunk("\r\n")
                                    return True
                            return False

                        def flush_using():
                            if current_using_fmt is not None and current_vals_for_using:
                                fmt = str(self.evaluate(current_using_fmt))
                                formatted = format_cpc_using(current_vals_for_using, fmt)
                                out.append(formatted)
                                print_chunk(formatted)
                                current_vals_for_using.clear()

                        for expr in stmt.expressions:
                            if isinstance(expr, Literal) and expr.type == 'USING_FMT':
                                flush_using()
                                current_using_fmt = expr.value
                                continue
                            elif isinstance(expr, Literal) and expr.type == 'SEPARATOR':
                                if current_using_fmt is not None:
                                    newline = False
                                elif expr.value == ';':
                                    newline = False
                                elif expr.value == ',':
                                    z = getattr(self, 'zone_width', 13)
                                    col = self.get_stream_pos(stream)
                                    spaces = z - ((col - 1) % z)
                                    if not poss_validate_xpos(spaces + z):
                                        sp_str = " " * spaces
                                        out.append(sp_str)
                                        print_chunk(sp_str)
                                    newline = False
                            elif isinstance(expr, Literal) and expr.type == 'SPC':
                                flush_using()
                                current_using_fmt = None
                                n = max(0, self.cint(self.evaluate(expr.value)))
                                w = self.get_stream_width(stream)
                                if w is not None and w > 0:
                                    n = n % w
                                sp_str = " " * n
                                out.append(sp_str)
                                print_chunk(sp_str)
                                newline = False
                            elif isinstance(expr, Literal) and expr.type == 'TAB':
                                flush_using()
                                current_using_fmt = None
                                n = self.cint(self.evaluate(expr.value)) - 1
                                if n < 0:
                                    n = 0
                                w = self.get_stream_width(stream)
                                if w is not None and w > 0:
                                    n = n % w
                                target_col = n + 1
                                curr_col = self.get_stream_pos(stream)
                                if target_col < curr_col:
                                    sp_str = " " * (target_col - 1)
                                    out.append("\n" + sp_str)
                                    print_chunk("\r\n" + sp_str)
                                else:
                                    sp_str = " " * (target_col - curr_col)
                                    out.append(sp_str)
                                    print_chunk(sp_str)
                                newline = False
                            else:
                                evaluated = self.evaluate(expr)
                                if current_using_fmt is not None:
                                    current_vals_for_using.append(evaluated)
                                else:
                                    if isinstance(evaluated, (int, float)):
                                        val = self.format_cpc_number(evaluated, with_leading_space=True) + " "
                                        poss_validate_xpos(len(val))
                                    else:
                                        val = str(evaluated)
                                        poss_validate_xpos(self._count_printable_prefix(val))
                                    out.append(val)
                                    print_chunk(val)
                                newline = True

                        flush_using()
                        if newline:
                            print_chunk("\r\n")

                        out_str = "".join(out)

                        if stream == 9 and hasattr(self, 'file_out') and 9 in self.file_out:
                            self.file_out[9].write(out_str + ("\n" if newline else ""))

                    elif isinstance(stmt, WriteStatement):
                        out = []
                        for expr in stmt.expressions:
                            if isinstance(expr, Literal) and expr.type == 'SEPARATOR':
                                continue
                            val = self.evaluate(expr)
                            if isinstance(val, str):
                                out.append(f'"{val}"')
                            else:
                                out.append(self.format_cpc_number(val, with_leading_space=False))
                        out_str = ",".join(out)
                        stream = self.cint(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) is not None else 0
                        target_stream = 0 if stream == 8 else stream
                        if stream == 9 and hasattr(self, 'file_out') and 9 in self.file_out:
                            self.file_out[9].write(out_str + "\n")
                        else:
                            self.display.print_text(out_str + "\r\n", target_stream)

                    elif isinstance(stmt, LocateStatement):
                        col = self.cint(self.evaluate(stmt.col))
                        row = self.cint(self.evaluate(stmt.row)) if getattr(stmt, 'row', None) else None
                        stream = self.cint(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) else 0
                        if row is not None:
                            self.display.locate(col, row, stream)
                        else:
                            curr_r = self.display.get_vpos(stream) if hasattr(self.display, 'get_vpos') else (self.display.streams[stream]['text_row'] if hasattr(self.display, 'streams') else self.display.text_row)
                            self.display.locate(col, curr_r, stream)
                    
                    elif isinstance(stmt, ClsStatement):
                        stream = self.cint(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) else 0
                        self.display.clear_graphics(stream)
                        self.display.locate(1, 1, stream)

                    elif isinstance(stmt, ClgStatement):
                        if stmt.color is not None:
                            c = self.cint(self.evaluate(stmt.color))
                            self.display.set_graphics_paper(c)
                        if hasattr(self.display, 'clear_graphics_window'):
                            self.display.clear_graphics_window()
                        else:
                            self.display.clear_graphics()
                        self.display.move(0, 0)

                    elif isinstance(stmt, BorderStatement):
                        col1 = self.cint(self.evaluate(stmt.color1))
                        col2 = self.cint(self.evaluate(stmt.color2)) if stmt.color2 else None
                        if hasattr(self.display, 'set_border'):
                            self.display.set_border(col1, col2)

                    elif isinstance(stmt, ClearStatement):
                        self.variables.clear()
                        self.arrays.clear()
                        self.for_loops.clear()
                        self.for_stack.clear()
                        self.gosub_stack.clear()
                        if hasattr(self, 'while_stack'):
                            self.while_stack.clear()
                        self.data_ptr = 0
                        self.angle_mode = 'RAD'

                    elif isinstance(stmt, ClearInputStatement):
                        if hasattr(self.display, 'clear_input'):
                            self.display.clear_input()
                        elif hasattr(self.display, 'key_buffer'):
                            self.display.key_buffer.clear()

                    elif isinstance(stmt, RandomizeStatement):
                        if stmt.expr:
                            val = self.evaluate(stmt.expr)
                            random.seed(val)
                        else:
                            random.seed()

                    elif isinstance(stmt, DegStatement):
                        self.angle_mode = 'DEG'

                    elif isinstance(stmt, RadStatement):
                        self.angle_mode = 'RAD'

                    elif isinstance(stmt, TagStatement):
                        stream = self.cint(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) is not None else 0
                        if stream == 0:
                            self.tag_active = True
                        if hasattr(self.display, 'set_tag'):
                            self.display.set_tag(True, stream)
                        elif hasattr(self.display, 'tag_active') and stream == 0:
                            self.display.tag_active = True

                    elif isinstance(stmt, TagoffStatement):
                        stream = self.cint(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) is not None else 0
                        if stream == 0:
                            self.tag_active = False
                        if hasattr(self.display, 'set_tag'):
                            self.display.set_tag(False, stream)
                        elif hasattr(self.display, 'tag_active') and stream == 0:
                            self.display.tag_active = False

                    elif isinstance(stmt, ZoneStatement):
                        z = self.cint(self.evaluate(stmt.width))
                        if 1 <= z <= 255:
                            self.zone_width = z
                        else:
                            next_pc = self.trigger_error(5, self.pc)
                            break

                    elif isinstance(stmt, MaskStatement):
                        if stmt.mask is not None:
                            mask = self.cint(self.evaluate(stmt.mask))
                            self.display.set_mask(mask)
                        if stmt.first_point is not None:
                            first_point = self.cint(self.evaluate(stmt.first_point))
                            self.display.set_mask_first(first_point)

                    elif isinstance(stmt, EraseStatement):
                        for var_name in stmt.arrays:
                            if var_name in self.arrays:
                                del self.arrays[var_name]

                    elif isinstance(stmt, AfterStatement):
                        delay = self.cint(self.evaluate(stmt.delay))
                        timer_id = self.cint(self.evaluate(stmt.timer_id)) if stmt.timer_id is not None else 0
                        target = self.cint(self.evaluate(stmt.line_number))
                        if 0 <= timer_id <= 3:
                            delay_ms = delay * 20 # 1/50th of a second
                            current_time = pygame.time.get_ticks() if 'pygame' in sys.modules else 0
                            self.timers[timer_id] = {
                                'type': 'AFTER',
                                'delay_ms': delay_ms,
                                'target': target,
                                'next_trigger': current_time + delay_ms
                            }
                        
                    elif isinstance(stmt, EveryStatement):
                        delay = self.cint(self.evaluate(stmt.ticks))
                        timer_id = self.cint(self.evaluate(stmt.timer_id)) if stmt.timer_id is not None else 0
                        target = self.cint(self.evaluate(stmt.line_number))
                        if 0 <= timer_id <= 3:
                            delay_ms = delay * 20 # 1/50th of a second
                            current_time = pygame.time.get_ticks() if 'pygame' in sys.modules else 0
                            self.timers[timer_id] = {
                                'type': 'EVERY',
                                'delay_ms': delay_ms,
                                'target': target,
                                'next_trigger': current_time + delay_ms
                            }

                    elif isinstance(stmt, LetArrayStatement):
                        if stmt.var_name.upper() in ('MID$', 'MID_STR'):
                            val = str(self.evaluate(stmt.expr))
                            target_var = stmt.dims[0].tokens[0].value
                            var_val = str(self.variables.get(target_var, ""))
                            start = self.cint(self.evaluate(stmt.dims[1]))
                            if len(stmt.dims) >= 3:
                                length = self.cint(self.evaluate(stmt.dims[2]))
                            else:
                                length = len(val)
                        
                            replace_str = val[:length]
                            new_str = var_val[:start-1] + replace_str + var_val[start-1+len(replace_str):]
                            if len(new_str) > len(var_val):
                                new_str = new_str[:len(var_val)]
                        
                            self.variables[target_var] = new_str
                        else:
                            val = self.evaluate(stmt.expr)
                            dims_eval = tuple(self.cint(self.evaluate(d)) for d in stmt.dims)
                            if stmt.var_name not in self.arrays:
                                self.arrays[stmt.var_name] = {}
                            self.arrays[stmt.var_name][dims_eval] = self.typecast(stmt.var_name, val)

                    elif isinstance(stmt, LetStatement):
                        val = self.evaluate(stmt.expr)
                        if stmt.identifier.startswith('_REG_'):
                            setattr(self.z80, stmt.identifier[5:], self.cint(val))
                        elif stmt.identifier == 'TIME':
                            self.set_cpc_time(val)
                        else:
                            self.variables[stmt.identifier] = self.typecast(stmt.identifier, val)
                    
                    elif isinstance(stmt, DimStatement):
                        for var_name, dims in stmt.arrays:
                            self.arrays[var_name] = {}
                    
                    elif isinstance(stmt, WhileStatement):
                        cond = self.evaluate(stmt.condition)
                        if cond:
                            if not hasattr(self, 'while_stack'):
                                self.while_stack = []
                            self.while_stack.append((self.pc, stmt_idx - 1))
                        else:
                            depth = 1
                            found = False
                            for s_i in range(stmt_idx, len(statements)):
                                s = statements[s_i]
                                if isinstance(s, WhileStatement):
                                    depth += 1
                                elif isinstance(s, WendStatement):
                                    depth -= 1
                                    if depth == 0:
                                        stmt_idx = s_i + 1
                                        found = True
                                        break
                            if not found:
                                idx = self.line_numbers.index(self.pc) + 1
                                while idx < len(self.line_numbers):
                                    line = self.line_numbers[idx]
                                    line_stmts = self.program.lines[line]
                                    for s_i, s in enumerate(line_stmts):
                                        if isinstance(s, WhileStatement):
                                            depth += 1
                                        elif isinstance(s, WendStatement):
                                            depth -= 1
                                            if depth == 0:
                                                next_pc = line
                                                self.next_stmt_idx = s_i + 1
                                                found = True
                                                break
                                    if found:
                                        break
                                    idx += 1
                                if found:
                                    break

                    elif isinstance(stmt, WendStatement):
                        if hasattr(self, 'while_stack') and self.while_stack:
                            loop_target = self.while_stack.pop()
                            if isinstance(loop_target, tuple):
                                loop_pc, loop_idx = loop_target
                            else:
                                loop_pc, loop_idx = loop_target, 0
                            if loop_pc == self.pc:
                                self.sound.update_queues()
                                if self._has_pending_interrupt():
                                    next_pc = loop_pc
                                    self.next_stmt_idx = loop_idx
                                    self.restore_statements = statements
                                    break
                                stmt_idx = loop_idx
                            else:
                                next_pc = loop_pc
                                self.next_stmt_idx = loop_idx
                                break

                    elif isinstance(stmt, OnStatement):
                        val = self.cint(self.evaluate(stmt.expr))
                        if 1 <= val <= len(stmt.line_numbers):
                            target = self.cint(self.evaluate(stmt.line_numbers[val - 1]))
                            if target in self.program.lines:
                                if stmt.is_gosub:
                                    self.gosub_stack.append((self.pc, stmt_idx, False, statements))
                                next_pc = target
                                break
                            else:
                                next_pc = self.trigger_error(8, self.pc)
                                break

                    elif isinstance(stmt, OnErrorStatement):
                        self.error_handler_line = self.cint(self.evaluate(stmt.line_number))
                        if self.error_handler_line == 0:
                            self.error_handler_line = 0 # ON ERROR GOTO 0 disables handler
                            
                    elif isinstance(stmt, OnBreakStatement):
                        self.on_break_action = stmt.action
                        if stmt.line_number is not None:
                            self.on_break_line = self.cint(self.evaluate(stmt.line_number))
                    
                    elif isinstance(stmt, OnSqStatement):
                        channel = self.cint(self.evaluate(stmt.channel)) if stmt.channel is not None else 1
                        if channel not in (1, 2, 4):
                            next_pc = self.trigger_error(5, self.pc)
                            break
                        target_line = self.cint(self.evaluate(stmt.line_number))
                        c_id = 0 if (channel & 1) else (1 if (channel & 2) else 2)
                        if target_line == 0:
                            self.sq_targets[c_id] = 0
                            self.sound.sq_events_armed[c_id] = False
                            self.sound.sq_events_pending[c_id] = False
                        else:
                            if target_line not in self.program.lines:
                                next_pc = self.trigger_error(8, self.pc)
                                break
                            self.sq_targets[c_id] = target_line
                            self.sound.arm_sq_event(channel)
                            if self.interrupts_enabled and self.sound.sq_events_pending.get(c_id, False) and stmt_idx < len(statements):
                                next_pc = self.pc
                                self.next_stmt_idx = stmt_idx
                                self.restore_statements = statements
                                break

                    elif isinstance(stmt, ErrorStatement):
                        code = self.cint(self.evaluate(stmt.code))
                        next_pc = self.trigger_error(code, self.pc)
                        break
                    
                    elif isinstance(stmt, ResumeStatement):
                        if stmt.is_next:
                            next_pc = self.get_next_line(self.pc)
                        elif stmt.line_number is not None:
                            next_pc = self.cint(self.evaluate(stmt.line_number))
                        else:
                            next_pc = self.err_line if self.err_line else self.pc
                        break
                    
                    elif isinstance(stmt, CallStatement):
                        addr = self.evaluate(stmt.address)
                        if isinstance(addr, str):
                            if addr.startswith('0x') or addr.startswith('0X'):
                                addr = int(addr, 16)
                            elif addr.startswith('&'):
                                val = addr[1:].upper()
                                if val.startswith('H'): val = val[1:]
                                addr = int(val, 16)
                            else:
                                try: addr = int(addr)
                                except: addr = 0
                        else:
                            try: addr = self.cint(addr)
                            except: addr = 0

                        if stmt.params:
                            try:
                                self.z80.A = self.cint(self.evaluate(stmt.params[0]))
                            except Exception:
                                self.z80.A = len(stmt.params)
                        else:
                            self.z80.A = 0

                        if addr == 0:
                            self.running = False
                            break
                        elif addr in self.firmware_hooks:
                            self.firmware_hooks[addr]()
                        elif 0 <= addr <= 65530 and self.ram[addr + 3] == 0xC3:
                            fw_addr = self.ram[addr + 4] | (self.ram[addr + 5] << 8)
                            if fw_addr in self.firmware_hooks:
                                self.firmware_hooks[fw_addr]()
                            else:
                                print(f"Warning: Unimplemented CALL &{addr:04X}")
                        elif not self.execute_machine_code(addr):
                            print(f"Warning: Unimplemented CALL &{addr:04X}")

                    elif isinstance(stmt, GotoStatement):
                        target = self.cint(self.evaluate(stmt.line_number))
                        if target in self.program.lines:
                            next_pc = target
                            break
                        else:
                            self.trigger_error(8, self.pc)
                            break
                        
                    elif isinstance(stmt, GosubStatement):
                        target = self.cint(self.evaluate(stmt.line_number))
                        if target in self.program.lines:
                            self.gosub_stack.append((self.pc, stmt_idx, False, statements))
                            next_pc = target
                            break
                        else:
                            self.trigger_error(8, self.pc)
                            break
                        
                    elif isinstance(stmt, ReturnStatement):
                        if self.gosub_stack:
                            ret_val = self.gosub_stack.pop()
                            if isinstance(ret_val, tuple):
                                if len(ret_val) == 4:
                                    next_pc, self.next_stmt_idx, is_interrupt, restored = ret_val
                                    if restored is not None:
                                        self.restore_statements = restored
                                elif len(ret_val) == 3:
                                    next_pc, self.next_stmt_idx, is_interrupt = ret_val
                                else:
                                    next_pc, is_interrupt = ret_val
                                if is_interrupt:
                                    self.interrupts_enabled = True
                            else:
                                next_pc = ret_val
                            break
                        else:
                            print(f"RETURN without GOSUB in {self.pc}")
                            self.running = False
                            break
                        

                    elif isinstance(stmt, SaveStatement):
                        filename = str(self.evaluate(stmt.filename))
                        print(f"[DISK] SAVE '{filename}'")

                    elif isinstance(stmt, LoadStatement):
                        filename = str(self.evaluate(stmt.filename))
                        print(f"[DISK] LOAD '{filename}'")
                        if filename.lower().startswith('!hr'):
                            self.ram[40000] = 0xC9

                    elif isinstance(stmt, EndStatement):
                        self.running = False
                        break
                        
                    elif isinstance(stmt, ModeStatement):
                        mode = int(self.evaluate(stmt.mode_expr))
                        print(f"[VIDEO] Setting MODE {mode}")
                        self.display.set_mode(mode)
                    
                    elif isinstance(stmt, OutStatement):
                        port = self.cint(self.evaluate(stmt.port)) & 0xFFFF
                        value = self.cint(self.evaluate(stmt.value)) & 0xFF
                        # Soporte de acceso directo al PSG AY-3-8912 vía PPI 8255 (&F4xx Puerto A, &F6xx Puerto C)
                        if (port & 0xFF00) == 0xF400:
                            self._ppi_port_a = value
                        elif (port & 0xFF00) == 0xF600:
                            bdir_bc1 = (value >> 6) & 0x03
                            if bdir_bc1 == 0x03:
                                self._psg_selected_reg = self._ppi_port_a & 0x0F
                            elif bdir_bc1 == 0x02:
                                self.sound.write_psg_register(getattr(self, '_psg_selected_reg', 0), self._ppi_port_a)

                    elif isinstance(stmt, WaitStatement):
                        port = int(self.evaluate(stmt.port))
                        mask = int(self.evaluate(stmt.mask))
                        invert = int(self.evaluate(stmt.invert)) if getattr(stmt, 'invert', None) is not None else 0
                        # stub wait

                    elif isinstance(stmt, CursorStatement):
                        stream = self.cint(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) is not None else 0
                        s1 = self.cint(self.evaluate(stmt.switch)) if getattr(stmt, 'switch', None) is not None else None
                        s2 = self.cint(self.evaluate(stmt.switch2)) if getattr(stmt, 'switch2', None) is not None else None
                        if hasattr(self.display, 'set_cursor'):
                            self.display.set_cursor(s1, s2, stream)

                    elif isinstance(stmt, WidthStatement):
                        w = self.cint(self.evaluate(stmt.width))
                        if 1 <= w <= 255:
                            self.printer_width = w
                        else:
                            next_pc = self.trigger_error(5, self.pc)
                            break

                    elif isinstance(stmt, WindowSwapStatement):
                        s1 = self.cint(self.evaluate(stmt.stream1))
                        s2 = self.cint(self.evaluate(stmt.stream2))
                        if not (0 <= s1 <= 7 and 0 <= s2 <= 7):
                            next_pc = self.trigger_error(5, self.pc)
                            break
                        if hasattr(self.display, 'streams'):
                            tmp = self.display.streams.get(s1, {})
                            self.display.streams[s1] = self.display.streams.get(s2, {})
                            self.display.streams[s2] = tmp

                    elif isinstance(stmt, ListStatement):
                        stream = self.cint(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) is not None else 0
                        target_stream = 0 if stream == 8 else stream
                        s_line = self.cint(self.evaluate(stmt.start_line)) if getattr(stmt, 'start_line', None) is not None else 0
                        e_line = self.cint(self.evaluate(stmt.end_line)) if getattr(stmt, 'end_line', None) is not None else 65535
                        source_lines = getattr(self.program, 'source_lines', {})
                        for ln in self.line_numbers:
                            if s_line <= ln <= e_line:
                                line_txt = source_lines.get(ln, str(ln))
                                if stream == 9 and hasattr(self, 'file_out') and 9 in self.file_out:
                                    self.file_out[9].write(line_txt + "\n")
                                elif hasattr(self, 'display'):
                                    self.display.print_text(line_txt + "\r\n", target_stream)

                    elif isinstance(stmt, AutoStatement):
                        line_num = int(self.evaluate(stmt.line_number)) if getattr(stmt, 'line_number', None) else 10
                        step = int(self.evaluate(stmt.step)) if getattr(stmt, 'step', None) else 10
                        self.display.print(f"AUTO {line_num},{step} - Use IDE Editor instead\r\n")

                    elif isinstance(stmt, CatStatement):
                        dsk = getattr(self, 'dsk', None)
                        if dsk and getattr(dsk, 'mounted', False):
                            files = dsk.list_files()
                            self.display.print("Drive A:\r\n")
                            for f in files:
                                self.display.print(f + "\r\n")
                            self.display.print(f"{len(files)} file(s)\r\n")
                        else:
                            self.display.print("Drive A: disc missing\r\n")

                    elif isinstance(stmt, ChainStatement):
                        filename = str(self.evaluate(stmt.filename))
                        dsk = getattr(self, 'dsk', None)
                        if dsk and getattr(dsk, 'mounted', False):
                            code = dsk.read_file(filename)
                            if code:
                                if not stmt.is_merge:
                                    self.program.lines.clear()
                            
                                from core.lexer import Lexer
                                from core.parser import Parser
                                l = Lexer(code)
                                p = Parser(l.tokens)
                                new_prog = p.parse()
                                for ln, stmts in new_prog.lines.items():
                                    self.program.lines[ln] = stmts
                                self.line_numbers = sorted(list(self.program.lines.keys()))
                            
                                if getattr(stmt, 'line_number', None):
                                    target_ln = int(self.evaluate(stmt.line_number))
                                    if target_ln in self.line_numbers:
                                        self.pc = target_ln
                                    else:
                                        self.pc = self.line_numbers[0] if self.line_numbers else None
                                else:
                                    self.pc = self.line_numbers[0] if self.line_numbers else None
                                break
                            else:
                                self.display.print(f"File '{filename}' not found\r\n")
                        else:
                            self.display.print("Drive A: disc missing\r\n")

                    elif isinstance(stmt, DeleteStatement):
                        s_line = int(self.evaluate(stmt.start_line)) if getattr(stmt, 'start_line', None) else 0
                        e_line = int(self.evaluate(stmt.end_line)) if getattr(stmt, 'end_line', None) else 65535
                        lines_to_delete = [ln for ln in self.line_numbers if s_line <= ln <= e_line]
                        for ln in lines_to_delete:
                            del self.program.lines[ln]
                        self.line_numbers = sorted(list(self.program.lines.keys()))
                        self.display.print("Deleted.\r\n")

                    elif isinstance(stmt, EditStatement):
                        self.display.print(f"EDIT - Use IDE Editor instead\r\n")

                    elif isinstance(stmt, MemoryStatement):
                        addr = int(self.evaluate(stmt.address))
                        self.builtins["HIMEM"] = lambda: addr

                    elif isinstance(stmt, MergeStatement):
                        filename = str(self.evaluate(stmt.filename))
                        dsk = getattr(self, 'dsk', None)
                        if dsk and getattr(dsk, 'mounted', False):
                            code = dsk.read_file(filename)
                            if code:
                                from core.lexer import Lexer
                                from core.parser import Parser
                                l = Lexer(code)
                                p = Parser(l.tokens)
                                new_prog = p.parse()
                                for ln, stmts in new_prog.lines.items():
                                    self.program.lines[ln] = stmts
                                self.line_numbers = sorted(list(self.program.lines.keys()))
                            else:
                                self.display.print(f"File '{filename}' not found\r\n")
                        else:
                            self.display.print("Drive A: disc missing\r\n")

                    elif isinstance(stmt, RenumStatement):
                        new_st = int(self.evaluate(stmt.new_start)) if getattr(stmt, 'new_start', None) else 10
                        old_st = int(self.evaluate(stmt.old_start)) if getattr(stmt, 'old_start', None) else self.line_numbers[0] if self.line_numbers else 10
                        step = int(self.evaluate(stmt.step)) if getattr(stmt, 'step', None) else 10
                    
                        old_lines = [ln for ln in self.line_numbers if ln >= old_st]
                        mapping = {}
                        curr_new = new_st
                        for ln in old_lines:
                            mapping[ln] = curr_new
                            curr_new += step
                        
                        new_prog = {}
                        for ln in self.line_numbers:
                            if ln in mapping:
                                new_prog[mapping[ln]] = self.program.lines[ln]
                            else:
                                new_prog[ln] = self.program.lines[ln]
                        self.program.lines = new_prog
                        self.line_numbers = sorted(list(self.program.lines.keys()))
                        self.display.print("Renumbered.\r\n")

                    elif isinstance(stmt, SaveStatement):
                        filename = str(self.evaluate(stmt.filename))
                        self.display.print(f"SAVE '{filename}' - Use IDE Editor to save\r\n")

                    elif isinstance(stmt, LoadStatement):
                        filename = str(self.evaluate(stmt.filename))
                        self.display.print(f"LOAD '{filename}' - Use IDE Editor instead\r\n")

                    elif isinstance(stmt, SwapStatement):
                        # var1 and var2 are identifiers
                        var1 = stmt.var1.upper()
                        var2 = stmt.var2.upper()
                        v1 = self.variables.get(var1, 0)
                        v2 = self.variables.get(var2, 0)
                        self.variables[var1] = v2
                        self.variables[var2] = v1

                    elif isinstance(stmt, PlotStatement):
                        x = self.cint(self.evaluate(stmt.x))
                        y = self.cint(self.evaluate(stmt.y))
                        pen = None
                        if stmt.pen is not None:
                            pen = self.cint(self.evaluate(stmt.pen))
                            self.display.set_graphics_pen(pen)
                        if getattr(stmt, 'mode', None) is not None:
                            mode = self.cint(self.evaluate(stmt.mode))
                            self.display.set_graphics_write_mode(mode)
                        self.display.plot(x, y, pen)

                    elif isinstance(stmt, PlotrStatement):
                        x = self.cint(self.evaluate(stmt.x))
                        y = self.cint(self.evaluate(stmt.y))
                        pen = None
                        if stmt.pen is not None:
                            pen = self.cint(self.evaluate(stmt.pen))
                            self.display.set_graphics_pen(pen)
                        if getattr(stmt, 'mode', None) is not None:
                            mode = self.cint(self.evaluate(stmt.mode))
                            self.display.set_graphics_write_mode(mode)
                        curr_x = getattr(self.display, 'graphics_x', 0)
                        curr_y = getattr(self.display, 'graphics_y', 0)
                        self.display.plot(curr_x + x, curr_y + y, pen)

                    elif isinstance(stmt, DrawStatement):
                        x = self.cint(self.evaluate(stmt.x))
                        y = self.cint(self.evaluate(stmt.y))
                        pen = None
                        if stmt.pen is not None:
                            pen = self.cint(self.evaluate(stmt.pen))
                            self.display.set_graphics_pen(pen)
                        if getattr(stmt, 'mode', None) is not None:
                            mode = self.cint(self.evaluate(stmt.mode))
                            self.display.set_graphics_write_mode(mode)
                        self.display.draw(x, y, pen)

                    elif isinstance(stmt, DrawrStatement):
                        x = self.cint(self.evaluate(stmt.x))
                        y = self.cint(self.evaluate(stmt.y))
                        pen = None
                        if stmt.pen is not None:
                            pen = self.cint(self.evaluate(stmt.pen))
                            self.display.set_graphics_pen(pen)
                        if getattr(stmt, 'mode', None) is not None:
                            mode = self.cint(self.evaluate(stmt.mode))
                            self.display.set_graphics_write_mode(mode)
                        # DRAWR logic: relative to current position
                        curr_x = getattr(self.display, 'graphics_x', 0)
                        curr_y = getattr(self.display, 'graphics_y', 0)
                        self.display.draw(curr_x + x, curr_y + y, pen)

                    elif isinstance(stmt, MoveStatement):
                        x = self.cint(self.evaluate(stmt.x))
                        y = self.cint(self.evaluate(stmt.y))
                        if stmt.pen is not None:
                            pen = self.cint(self.evaluate(stmt.pen))
                            self.display.set_graphics_pen(pen)
                        if stmt.mode is not None:
                            mode = self.cint(self.evaluate(stmt.mode))
                            self.display.set_graphics_write_mode(mode)
                        self.display.move(x, y)

                    elif isinstance(stmt, MoverStatement):
                        x = self.cint(self.evaluate(stmt.x))
                        y = self.cint(self.evaluate(stmt.y))
                        if stmt.pen:
                            pen = self.cint(self.evaluate(stmt.pen))
                            self.display.set_graphics_pen(pen)
                        if getattr(stmt, 'mode', None) is not None:
                            mode = self.cint(self.evaluate(stmt.mode))
                            self.display.set_graphics_write_mode(mode)
                        curr_x = getattr(self.display, 'graphics_x', 0)
                        curr_y = getattr(self.display, 'graphics_y', 0)
                        self.display.move(curr_x + x, curr_y + y)
                    
                    elif isinstance(stmt, OriginStatement):
                        x = self.cint(self.evaluate(stmt.x))
                        y = self.cint(self.evaluate(stmt.y))
                        self.display.origin_x = x
                        self.display.origin_y = y
                        if stmt.left is not None:
                            left = self.cint(self.evaluate(stmt.left))
                            right = self.cint(self.evaluate(stmt.right))
                            top = self.cint(self.evaluate(stmt.top))
                            bottom = self.cint(self.evaluate(stmt.bottom))
                            if hasattr(self.display, 'set_graphics_window'):
                                self.display.set_graphics_window(left, right, top, bottom)

                    elif isinstance(stmt, FillStatement):
                        pen = self.cint(self.evaluate(stmt.pen))
                        if hasattr(self.display, 'fill'):
                            self.display.fill(pen)

                    elif isinstance(stmt, RsxStatement):
                        if stmt.command == 'SCREENSWAP':
                            args = [int(self.evaluate(p)) for p in stmt.params]
                            if len(args) == 2:
                                self.display.screenswap(args[0], args[1])
                            elif len(args) == 3:
                                self.display.screenswap(args[1], args[2], section=args[0])
                        elif stmt.command == 'SCREENCOPY':
                            args = [int(self.evaluate(p)) for p in stmt.params]
                            if len(args) == 2:
                                self.display.screencopy(args[0], args[1]) # dest, src
                        elif stmt.command == 'BANKOPEN':
                            args = [int(self.evaluate(p)) for p in stmt.params]
                            if len(args) > 0:
                                self.bank_record_length = args[0]
                            self.bank_current_record = 0
                        elif stmt.command == 'BANKWRITE':
                            # |BANKWRITE, @<codigo>, <cadena> [, <registro>]
                            if len(stmt.params) >= 2:
                                # First param should be the variable name, parsed as a literal string by parser for @vars
                                p0 = stmt.params[0]
                                err_var = p0.value if isinstance(p0, Literal) else p0.name if isinstance(p0, Variable) else str(self.evaluate(p0))
                                text = str(self.evaluate(stmt.params[1]))
                                if len(stmt.params) >= 3:
                                    self.bank_current_record = int(self.evaluate(stmt.params[2]))
                            
                                addr = self.bank_current_record * self.bank_record_length
                                if addr + self.bank_record_length > len(self.bank_memory):
                                    self.variables[err_var] = -1
                                else:
                                    chunk = text.encode('ascii', 'ignore')[:self.bank_record_length]
                                    self.bank_memory[addr:addr+len(chunk)] = chunk
                                    self.variables[err_var] = self.bank_current_record
                                    self.bank_current_record += 1
                        elif stmt.command == 'BANKREAD':
                            # |BANKREAD, @<codigo>, <cadena> [, <registro>]
                            if len(stmt.params) >= 2:
                                p0 = stmt.params[0]
                                err_var = p0.value if isinstance(p0, Literal) else p0.name if isinstance(p0, Variable) else str(self.evaluate(p0))
                                
                                p1 = stmt.params[1]
                                str_var = p1.name if isinstance(p1, Variable) else p1.value if isinstance(p1, Literal) else None

                                if str_var is not None:
                                    if len(stmt.params) >= 3:
                                        self.bank_current_record = int(self.evaluate(stmt.params[2]))
                                    
                                    addr = self.bank_current_record * self.bank_record_length
                                    if addr + self.bank_record_length > len(self.bank_memory):
                                        self.variables[err_var] = -1
                                    else:
                                        chunk = self.bank_memory[addr:addr+self.bank_record_length].decode('ascii', 'ignore')
                                        
                                        curr_val = self.variables.get(str_var, "")
                                        curr_len = len(curr_val)
                                        
                                        new_val = chunk[:curr_len]
                                        if len(new_val) < curr_len:
                                            new_val += curr_val[len(new_val):]
                                            
                                        self.variables[str_var] = new_val
                                        self.variables[err_var] = self.bank_current_record
                                        self.bank_current_record += 1
                        elif stmt.command == 'BANKFIND':
                            # |BANKFIND, @<codigo>, <cadena> [, <reg_inicio> [, <reg_fin>]]
                            if len(stmt.params) >= 2:
                                p0 = stmt.params[0]
                                err_var = p0.value if isinstance(p0, Literal) else p0.name if isinstance(p0, Variable) else str(self.evaluate(p0))
                                search = str(self.evaluate(stmt.params[1]))
                                start_reg = self.bank_current_record
                                end_reg = (65536 // self.bank_record_length) - 1
                                if len(stmt.params) >= 3:
                                    start_reg = int(self.evaluate(stmt.params[2]))
                                if len(stmt.params) >= 4:
                                    end_reg = int(self.evaluate(stmt.params[3]))
                                
                                found = False
                                for r in range(start_reg, end_reg + 1):
                                    addr = r * self.bank_record_length
                                    if addr + self.bank_record_length > len(self.bank_memory):
                                        break
                                    chunk = self.bank_memory[addr:addr+self.bank_record_length].decode('ascii', 'ignore')
                                    search_len = min(len(search), self.bank_record_length)
                                    match = True
                                    for i in range(search_len):
                                        if search[i] != '\x00' and i < len(chunk) and search[i] != chunk[i]:
                                            match = False
                                            break
                                    if match:
                                        self.variables[err_var] = r
                                        self.bank_current_record = r
                                        found = True
                                        break
                                if not found:
                                    self.variables[err_var] = -3
                                else:
                                    pass

                    elif isinstance(stmt, InkStatement):
                        pen = self.cint(self.evaluate(stmt.pen))
                        color1 = self.cint(self.evaluate(stmt.color1))
                        color2 = self.cint(self.evaluate(stmt.color2)) if stmt.color2 else None
                        self.display.set_ink(pen, color1, color2)

                    elif isinstance(stmt, PenStatement):
                        stream = self.cint(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) is not None else 0
                        bg_mode = self.cint(self.evaluate(stmt.bg_mode)) if getattr(stmt, 'bg_mode', None) is not None else None
                        if stmt.pen is not None:
                            pen = self.cint(self.evaluate(stmt.pen))
                            self.display.set_pen(pen, stream, bg_mode)
                        elif bg_mode is not None:
                            self.display.set_bg_mode(bg_mode, stream)

                    elif isinstance(stmt, PaperStatement):
                        paper = self.cint(self.evaluate(stmt.paper))
                        stream = self.cint(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) else 0
                        self.display.set_paper(paper, stream)
                    
                    elif type(stmt).__name__ == 'GraphicsPenStatement':
                        if stmt.pen is not None:
                            pen = self.cint(self.evaluate(stmt.pen))
                            self.display.set_graphics_pen(pen)
                        if stmt.bg_mode is not None:
                            bg_mode = self.cint(self.evaluate(stmt.bg_mode))
                            self.display.set_bg_mode(bg_mode)

                    elif type(stmt).__name__ == 'GraphicsPaperStatement':
                        paper = self.cint(self.evaluate(stmt.paper))
                        self.display.set_graphics_paper(paper)

                    elif isinstance(stmt, KeyStatement):
                        k_num = self.cint(self.evaluate(stmt.key_num))
                        k_str = str(self.evaluate(stmt.string_expr))
                        # Macro expansion not physically rendered in this version
                        
                    elif isinstance(stmt, KeyDefStatement):
                        k_num = self.cint(self.evaluate(stmt.key_num))
                        k_rep = self.cint(self.evaluate(stmt.repeat))
                        k_norm = self.cint(self.evaluate(stmt.normal)) if stmt.normal is not None else None
                        k_shift = self.cint(self.evaluate(stmt.shift)) if stmt.shift is not None else None
                        k_ctrl = self.cint(self.evaluate(stmt.control)) if stmt.control is not None else None
                        # Key definition not physically applied in this version

                    elif isinstance(stmt, SpeedStatement):
                        target = stmt.type
                        expr1 = stmt.params[0] if len(stmt.params) > 0 else None
                        expr2 = stmt.params[1] if len(stmt.params) > 1 else None
                        
                        if target == 'INK':
                            if expr1 is not None:
                                t1 = self.cint(self.evaluate(expr1))
                                t2 = self.cint(self.evaluate(expr2)) if expr2 is not None else t1
                                self.display.set_speed_ink(t1, t2)
                        elif target == 'KEY':
                            if expr1 is not None and expr2 is not None:
                                t1 = self.cint(self.evaluate(expr1))
                                t2 = self.cint(self.evaluate(expr2))
                                self.display.set_speed_key(t1, t2)
                        elif target == 'WRITE':
                            if expr1 is not None:
                                t1 = self.cint(self.evaluate(expr1))
                                self.speed_write = t1

                    elif isinstance(stmt, EnvStatement):
                        env_no = self.cint(self.evaluate(stmt.env_no))
                        if not (1 <= env_no <= 15):
                            next_pc = self.trigger_error(5, self.pc)
                            break
                        sections = [self.cint(self.evaluate(s)) for s in stmt.sections]
                        self.sound.set_env(env_no, sections)
                        self._sync_env_ram(env_no)
                    
                    elif isinstance(stmt, EntStatement):
                        ent_no = self.cint(self.evaluate(stmt.ent_no))
                        if ent_no == 0 or abs(ent_no) > 15:
                            next_pc = self.trigger_error(5, self.pc)
                            break
                        sections = [self.cint(self.evaluate(s)) for s in stmt.sections]
                        self.sound.set_ent(ent_no, sections)
                        self._sync_ent_ram(ent_no)

                    elif isinstance(stmt, SoundStatement):
                        channel = self.cint(self.evaluate(stmt.channel)) if stmt.channel is not None else 1
                        period = self.cint(self.evaluate(stmt.period)) if stmt.period is not None else 0
                        duration = self.cint(self.evaluate(stmt.duration)) if stmt.duration is not None else 20
                        volume = self.cint(self.evaluate(stmt.volume)) if stmt.volume is not None else 12
                        env = self.cint(self.evaluate(stmt.env)) if stmt.env is not None else 0
                        ent = self.cint(self.evaluate(stmt.ent)) if stmt.ent is not None else 0
                        noise = self.cint(self.evaluate(stmt.noise)) if stmt.noise is not None else 0

                        # Validaciones de rangos de Sound.asm (ROM BASIC 1.1)
                        if not (1 <= channel <= 255) or not (0 <= period <= 4095) or not (0 <= env <= 15) or not (-15 <= ent <= 15) or not (0 <= noise <= 31) or volume < 0 or volume > 15:
                            next_pc = self.trigger_error(5, self.pc)
                            break

                        # Espejo del bloque de 9 bytes de parámetros SOUND en RAM (&AD99..&ADA1)
                        dur_u16 = duration & 0xFFFF
                        self.ram[0xAD99] = channel & 0xFF
                        self.ram[0xAD9A] = env & 0xFF
                        self.ram[0xAD9B] = abs(ent) & 0xFF
                        self.ram[0xAD9C] = period & 0xFF
                        self.ram[0xAD9D] = (period >> 8) & 0x0F
                        self.ram[0xAD9E] = noise & 0x1F
                        self.ram[0xAD9F] = (volume & 0x0F) | 0x80
                        self.ram[0xADA0] = dur_u16 & 0xFF
                        self.ram[0xADA1] = (dur_u16 >> 8) & 0xFF

                        # Sound.asm líneas 48-53: si la cola está llena (Carry Clear), re-ejecutar la sentencia
                        # tras procesar eventos síncronos (AFTER/EVERY/ON SQ/ON BREAK) para evitar bloqueo
                        ok = self.sound.play_sound(channel, period, duration, volume, env, ent, noise, blocking=False)
                        if not ok:
                            if hasattr(self, 'display'):
                                self.display.process_events()
                                if getattr(self.display, 'quit_requested', False):
                                    self.running = False
                                    break
                            if 'pygame' in sys.modules:
                                pygame.time.wait(5)
                            next_pc = self.pc
                            self.next_stmt_idx = stmt_idx - 1
                            self.restore_statements = statements
                            break
                    
                    elif isinstance(stmt, ReleaseStatement):
                        channels = self.cint(self.evaluate(stmt.channels))
                        if not (1 <= channels <= 7):
                            next_pc = self.trigger_error(5, self.pc)
                            break
                        self.sound.release_channels(channels)
                    
                    elif isinstance(stmt, IfStatement):
                        cond_val = self.evaluate(stmt.condition)
                        branch_stmts = stmt.then_stmts if cond_val else getattr(stmt, 'else_stmts', [])
                    
                        if branch_stmts:
                            statements = statements[:stmt_idx] + branch_stmts + statements[stmt_idx:]
                    elif isinstance(stmt, ForStatement):
                        start_val = self.evaluate(stmt.start_expr)
                        end_val = self.evaluate(stmt.end_expr)
                        step_val = self.evaluate(stmt.step_expr)
                    
                        self.variables[stmt.identifier] = self.typecast(stmt.identifier, start_val)
                        next_pos = self._find_matching_next(stmt.identifier, self.pc, statements, stmt_idx)
                        match_next_pos = (next_pos[0], next_pos[1] - 1) if next_pos else None
                        if (step_val > 0 and start_val > end_val) or (step_val < 0 and start_val < end_val):
                            if stmt.identifier in self.for_stack:
                                self.for_stack.remove(stmt.identifier)
                            self.for_loops.pop(stmt.identifier, None)
                            if next_pos:
                                target_pc, target_idx = next_pos
                                if target_pc == self.pc:
                                    stmt_idx = target_idx
                                else:
                                    next_pc = target_pc
                                    self.next_stmt_idx = target_idx
                                    break
                            else:
                                self.trigger_error(26, self.pc)
                                break
                        else:
                            if stmt.identifier in self.for_stack:
                                idx_in_stack = self.for_stack.index(stmt.identifier)
                                for abandoned_var in self.for_stack[idx_in_stack:]:
                                    self.for_loops.pop(abandoned_var, None)
                                self.for_stack = self.for_stack[:idx_in_stack]
                            self.for_loops[stmt.identifier] = ((self.pc, stmt_idx), end_val, step_val, match_next_pos)
                            self.for_stack.append(stmt.identifier)
                    
                    elif isinstance(stmt, ReadStatement):
                        for var in stmt.variables:
                            if self.data_ptr < len(self.data_values):
                                _, val_expr = self.data_values[self.data_ptr]
                                val = self.evaluate(val_expr)
                                if isinstance(var, tuple):
                                    var_name, dims = var
                                    dims_eval = tuple(self.cint(self.evaluate(d)) for d in dims)
                                    if var_name not in self.arrays:
                                        self.arrays[var_name] = {}
                                    self.arrays[var_name][dims_eval] = self.typecast(var_name, val)
                                else:
                                    self.variables[var] = self.typecast(var, val)
                                self.data_ptr += 1
                            else:
                                print(f"DATA exhausted at {self.pc}")
                                self.running = False
                                break

                    elif isinstance(stmt, RestoreStatement):
                        if stmt.line_number is not None:
                            target_line = self.cint(self.evaluate(stmt.line_number))
                            found = False
                            for i, (ln, _) in enumerate(self.data_values):
                                if ln >= target_line:
                                    self.data_ptr = i
                                    found = True
                                    break
                            if not found:
                                self.data_ptr = len(self.data_values)
                        else:
                            self.data_ptr = 0

                    elif type(stmt).__name__ == 'DefTypeStatement':
                        for start_char, end_char in stmt.ranges:
                            for char_code in range(ord(start_char), ord(end_char) + 1):
                                if stmt.type_name == 'DEFINT':
                                    self.default_types[chr(char_code)] = 'INT'
                                elif stmt.type_name == 'DEFREAL':
                                    self.default_types[chr(char_code)] = 'REAL'
                                elif stmt.type_name == 'DEFSTR':
                                    self.default_types[chr(char_code)] = 'STR'

                    elif type(stmt).__name__ == 'DiStatement':
                        self.interrupts_enabled = False

                    elif type(stmt).__name__ == 'EiStatement':
                        self.interrupts_enabled = True

                    elif type(stmt).__name__ == 'DefFnStatement':
                        # We store a lambda that evaluates the expression when called
                        # To capture current context, we use a default arg or just reference self
                        # We need to map parameters to variables temporarily when called
                        def create_fn(params, expr):
                            def fn(*args):
                                # Save old variable values
                                old_vars = {}
                                for i, param in enumerate(params):
                                    if i < len(args):
                                        old_vars[param] = self.variables.get(param, 0)
                                        self.variables[param] = args[i]
                            
                                # Evaluate
                                result = self.evaluate(expr)
                            
                                # Restore old variable values
                                for param, old_val in old_vars.items():
                                    self.variables[param] = old_val
                                
                                return result
                            return fn
                        
                        self.user_functions[stmt.name.upper()] = create_fn(stmt.params, stmt.expr)

                    elif isinstance(stmt, StopStatement):
                        print("STOP at line", self.pc)
                        self.running = False
                        break

                    elif type(stmt).__name__ == 'OpenInStatement':
                        filename = str(self.evaluate(stmt.filename))
                        if not hasattr(self, 'file_in'): self.file_in = {}
                        try:
                            self.file_in[9] = open(filename, "r", encoding="utf-8")
                        except Exception as e:
                            print(f"Error opening {filename}: {e}")

                    elif type(stmt).__name__ == 'OpenOutStatement':
                        filename = str(self.evaluate(stmt.filename))
                        if not hasattr(self, 'file_out'): self.file_out = {}
                        try:
                            self.file_out[9] = open(filename, "w", encoding="utf-8")
                        except Exception as e:
                            print(f"Error opening {filename}: {e}")

                    elif type(stmt).__name__ == 'CloseInStatement':
                        if hasattr(self, 'file_in') and 9 in self.file_in:
                            self.file_in[9].close()
                            del self.file_in[9]

                    elif type(stmt).__name__ == 'CloseOutStatement':
                        if hasattr(self, 'file_out') and 9 in self.file_out:
                            self.file_out[9].close()
                            del self.file_out[9]

                    elif isinstance(stmt, InputStatement):
                        stream = self.cint(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) is not None else 0
                        if stream == 9 and hasattr(self, 'file_in') and 9 in self.file_in:
                            # read from file
                            val = self.file_in[9].readline()
                            if val.endswith("\n"): val = val[:-1]
                            if val.endswith("\r"): val = val[:-1]
                        else:
                            if stmt.prompt:
                                self.display.print_text(stmt.prompt)
                                self.display.update()
                            val = self.display.input_string()
                            print(f"[INPUT] user entered: {val}")
                        
                        if stmt.variables:
                            input_parts = val.split(',')
                            for i, var in enumerate(stmt.variables):
                                if i < len(input_parts):
                                    part_val = input_parts[i].strip()
                                else:
                                    part_val = ""
                                parsed_val = part_val
                            
                                is_array = isinstance(var, tuple)
                                var_name = var[0] if is_array else var
                            
                                if not var_name.endswith('$'):
                                    val_str = part_val.upper()
                                    try:
                                        if val_str.startswith('&X'):
                                            parsed_val = int(val_str[2:], 2)
                                        elif val_str.startswith('&H'):
                                            parsed_val = int(val_str[2:], 16)
                                        elif val_str.startswith('&'):
                                            parsed_val = int(val_str[1:], 16)
                                        else:
                                            parsed_val = float(val_str) if '.' in val_str else int(val_str)
                                    except ValueError:
                                        parsed_val = 0
                                    
                                if is_array:
                                    var_name, dims = var
                                    dims_eval = tuple(self.cint(self.evaluate(d)) for d in dims)
                                    if var_name not in self.arrays:
                                        self.arrays[var_name] = {}
                                    self.arrays[var_name][dims_eval] = self.typecast(var_name, parsed_val)
                                else:
                                    self.variables[var_name] = parsed_val

                    elif isinstance(stmt, FrameStatement):
                        if 'pygame' in sys.modules:
                            if hasattr(self, 'display'):
                                self.display.update()
                                self.last_update = pygame.time.get_ticks()
                            pygame.time.wait(20)

                    elif isinstance(stmt, SymbolAfterStatement):
                        limit = self.cint(self.evaluate(stmt.limit))
                        if hasattr(self, 'display') and hasattr(self.display, 'symbol_after'):
                            self.display.symbol_after(limit)
                        self.init_font_ram()

                    elif isinstance(stmt, SymbolStatement):
                        char_code = self.cint(self.evaluate(stmt.char_code))
                        matrix = [self.cint(self.evaluate(m)) for m in stmt.matrix]
                        while len(matrix) < 8:
                            matrix.append(0)
                        matrix = matrix[:8]
                        if hasattr(self.display, 'define_symbol'):
                            self.display.define_symbol(char_code, matrix)
                        for idx, b in enumerate(matrix):
                            ram_addr = 42597 + char_code * 8 + idx
                            if ram_addr < len(self.ram):
                                self.ram[ram_addr] = b

                    elif isinstance(stmt, WindowStatement):
                        left = self.cint(self.evaluate(stmt.left))
                        right = self.cint(self.evaluate(stmt.right))
                        top = self.cint(self.evaluate(stmt.top))
                        bottom = self.cint(self.evaluate(stmt.bottom))
                        stream = self.cint(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) else 0
                        if hasattr(self.display, 'set_window'):
                            self.display.set_window(left, right, top, bottom, stream)

                    elif isinstance(stmt, PokeStatement):
                        addr = self.cint(self.evaluate(stmt.address)) & 0xFFFF
                        val = self.cint(self.evaluate(stmt.value)) & 0xFF
                        self.ram[addr] = val
                        if addr >= 0xC000:
                            self.display.poke_video_ram(addr, val)
                        elif 0xB2B6 <= addr < 0xB3A6:
                            env_no = (addr - 0xB2A6) // 16
                            base = 0xB2A6 + 16 * env_no
                            self.sound.set_env_from_ram(env_no, bytes(self.ram[base:base + 16]))
                        elif 0xB3A6 <= addr < 0xB496:
                            ent_no = (addr - 0xB396) // 16
                            base = 0xB396 + 16 * ent_no
                            self.sound.set_ent_from_ram(ent_no, bytes(self.ram[base:base + 16]))
                        
                    elif isinstance(stmt, NextStatement):
                        identifiers = getattr(stmt, 'identifiers', [stmt.identifier])
                        curr_next_pos = (self.pc, stmt_idx - 1)
                    
                        next_jump = None
                        for var_name in identifiers:
                            if not var_name and self.for_stack:
                                matched_var = None
                                for candidate in reversed(self.for_stack):
                                    info = self.for_loops.get(candidate)
                                    if info and len(info) >= 4 and info[3] == curr_next_pos:
                                        matched_var = candidate
                                        break
                                var_name = matched_var if matched_var is not None else self.for_stack[-1]
                            
                            if var_name in self.for_loops:
                                if var_name in self.for_stack:
                                    idx_in_stack = self.for_stack.index(var_name)
                                    for abandoned_var in self.for_stack[idx_in_stack + 1:]:
                                        self.for_loops.pop(abandoned_var, None)
                                    self.for_stack = self.for_stack[:idx_in_stack + 1]
                                loop_info = self.for_loops[var_name]
                                loop_target, end_val, step_val = loop_info[0], loop_info[1], loop_info[2]
                                current_val = self.variables.get(var_name, 0)
                            
                                next_val = self.typecast(var_name, current_val + step_val)
                                self.variables[var_name] = next_val
                            
                                if (step_val > 0 and next_val <= end_val) or (step_val < 0 and next_val >= end_val):
                                    next_jump = loop_target
                                    break # Do not process subsequent variables yet, we loop back
                                else:
                                    del self.for_loops[var_name]
                                    if var_name in self.for_stack:
                                        self.for_stack.remove(var_name)
                    
                        if next_jump is not None:
                            if isinstance(next_jump, tuple):
                                jump_pc, jump_idx = next_jump
                            else:
                                jump_pc, jump_idx = next_jump, 0
                            if jump_pc == self.pc:
                                self.sound.update_queues()
                                if self._has_pending_interrupt():
                                    next_pc = jump_pc
                                    self.next_stmt_idx = jump_idx
                                    self.restore_statements = statements
                                    break
                                stmt_idx = jump_idx
                            else:
                                next_pc = jump_pc
                                self.next_stmt_idx = jump_idx
                                break
            except BasicErrorInterrupt:
                self.err_stmt_idx = getattr(self, '_current_stmt_idx', 0)
                if getattr(self, 'error_handler_line', 0) > 0 and self.error_handler_line in self.program.lines:
                    next_pc = self.error_handler_line
                    self.next_stmt_idx = 0
                else:
                    print(f"Error {getattr(self, 'err_code', 0)} in line {getattr(self, 'err_line', 0)}")
                    self.running = False
                    break
            self.pc = next_pc
            
        # Keep window open when execution finishes
        if hasattr(self, 'display'):
            self.display.update()


