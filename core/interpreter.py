import math
import random
import sys
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
                         RsxStatement, OnErrorStatement, ErrorStatement, ResumeStatement, OnBreakStatement, OnSqStatement, CallStatement, ReleaseStatement, OutStatement, WaitStatement, CursorStatement, PlotrStatement, WidthStatement, WindowSwapStatement, SwapStatement, AutoStatement, CatStatement, ChainStatement, DeleteStatement, EditStatement, MemoryStatement, MergeStatement, RenumStatement, SaveStatement, LoadStatement)
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
        self.data_values = []
        self.data_ptr = 0
        self.user_functions = {}
        self.default_types = {chr(c): 'REAL' for c in range(ord('A'), ord('Z')+1)}
        self.interrupts_enabled = True
        self.angle_mode = 'RAD'
        self.tag_active = False
        self.err_code = 0
        self.err_line = 0
        if hasattr(self, 'display'):
            import pygame
            if pygame.display.get_surface() is None:
                pygame.display.init()
                self.display.screen = pygame.display.set_mode((self.display.width * self.display.scale, self.display.height * self.display.scale))
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
        self.sound = SoundEngine()
        
        # Z80 Ghost Registers
        self.z80 = Z80Registers()
        
        self.firmware_hooks = {
            0xBB5A: self.fw_txt_output,
            0xBB18: self.fw_km_wait_char,
            0xBB06: self.fw_km_wait_char,
            0xBB75: self.fw_txt_set_cursor,
            0xBB78: self.fw_txt_get_cursor,
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
            0xBCAA: self.fw_sound_queue,
            0xBCA7: self.fw_sound_check,
            0xBD19: self.fw_mc_wait_flyback,
            0xBC14: self.fw_scr_clear
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
        
        self.err_code = 0
        self.err_line = 0
        self.error_handler_line = 0
        
        # Virtual 64KB RAM for PEEK/POKE
        self.ram = bytearray(65536)
        
        # Bank RAM for RSX
        self.bank_record_length = 255
        self.bank_current_record = 0
        self.bank_memory = bytearray(65536)

        # Funciones built-in del Amstrad BASIC para el evaluador
        self.builtins = {
            "__builtins__": None,
            "SIN": lambda x: math.sin(math.radians(x) if self.angle_mode == 'DEG' else x),
            "COS": lambda x: math.cos(math.radians(x) if self.angle_mode == 'DEG' else x),
            "TAN": lambda x: math.tan(math.radians(x) if self.angle_mode == 'DEG' else x),
            "INT": math.floor,
            "ABS": abs,
            "RND": self.cpc_rnd,
            "PI": math.pi,
            "TIME": lambda: int(pygame.time.get_ticks() / 3.33) if 'pygame' in sys.modules else 0,
            "XPOS": lambda: self.display.graphics_x,
            "YPOS": lambda: self.display.graphics_y,
            "VPOS": lambda: self.display.text_row,
            "CHR_STR": cpc_chr,
            "ASC": cpc_asc,
            "SQR": math.sqrt,
            "LOG": math.log,
            "LOG10": math.log10,
            "VAL": lambda x: float(x) if '.' in str(x) else int(x) if str(x).lstrip('-').isdigit() else 0,
            "RIGHT_STR": lambda s, n: s[-int(n):] if int(n) > 0 else "",
            "MID_STR": lambda s, start, n=None: s[int(start)-1:int(start)-1+int(n)] if n is not None else s[int(start)-1:],
            "LOWER_STR": lambda s: s.lower(),
            "MAX": max,
            "SQ": lambda x: self.sound.get_sq_status(int(x)),
            "LEN": len,
            "TEST": lambda x, y: self.display.test(x, y) if hasattr(self.display, 'test') else 0,
            "TESTR": lambda x, y: self.display.test(self.display.graphics_x + x, self.display.graphics_y + y) if hasattr(self.display, 'test') else 0,
            "REMAIN": lambda x: 0,
            "INKEY": lambda key: self.display.get_inkey_state(int(key)),
            "COPYCHR_STR": lambda stream: self.display.copychr(stream) if hasattr(self.display, 'copychr') else "",
            "CREAL": float,
            "CINT": lambda x: int(self.cpc_round(x)),
            "ERR": lambda: self.err_code,
            "ERL": lambda: self.err_line,
            "FIX": int,
            "ROUND": lambda x, d=0: self.cpc_round(x, d) if d > 0 else int(self.cpc_round(x, d)),
            "UNT": lambda x: (int(x) & 0xFFFF) - 65536 if (int(x) & 0xFFFF) >= 32768 else (int(x) & 0xFFFF),
            "LEFT_STR": lambda s, n: s[:int(n)] if int(n) > 0 else "",
            "UPPER_STR": lambda s: s.upper(),
            "STR_STR": lambda x: f" {x}" if x >= 0 else str(x),
            "SPACE_STR": lambda n: " " * int(n),
            "STRING_STR": lambda n, c: (chr(int(c)) if isinstance(c, (int, float)) else c[0]) * int(n),
            "HEX_STR": lambda x, w=None: hex(int(x))[2:].upper().zfill(w) if w else hex(int(x))[2:].upper(),
            "BIN_STR": lambda x, w=None: bin(int(x))[2:].zfill(w) if w else bin(int(x))[2:],
            "INSTR": lambda a, b, c=None: b.find(c, int(a)-1) + 1 if c is not None else a.find(b) + 1,
            "PEEK": self.do_peek,
            "JOY": lambda joy_id: self.get_joy_state(int(joy_id)),
            "ATN": lambda x: math.degrees(math.atan(x)) if self.angle_mode == 'DEG' else math.atan(x),
            "SGN": lambda x: 1 if x > 0 else (-1 if x < 0 else 0),
            "MIN": min,
            "EXP": math.exp,
            "DEC_STR": lambda x, fmt: format_cpc_field(x, str(fmt)) if isinstance(fmt, str) else str(x),
            "SPC": lambda x: " " * int(x),
            "TAB": lambda x: " " * max(0, int(x) - self.display.streams[0]["text_col"]) if hasattr(self, 'display') and hasattr(self.display, 'streams') else " " * max(0, int(x) - 1),
            "EOF": self.check_eof
        }
        
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

    def cpc_round(self, x, d=0):
        m = 10 ** d
        return math.floor(x * m + 0.5) / m if d > 0 else math.floor(x + 0.5)

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

    def do_peek(self, addr):
        addr = int(addr) & 0xFFFF
        if addr >= 0xC000:
            return self.display.peek_video_ram(addr)
        return self.ram[addr]

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
        
    def fw_sound_queue(self):
        addr = self.z80.HL
        if addr + 8 > 65535:
            return
            
        status = self.ram[addr]
        env = self.ram[addr+1]
        ent = self.ram[addr+2]
        period = self.ram[addr+3] | (self.ram[addr+4] << 8)
        noise = self.ram[addr+5]
        volume = self.ram[addr+6]
        duration = self.ram[addr+7] | (self.ram[addr+8] << 8)
        
        # Convert duration to 16-bit signed
        duration = self._to_signed16(duration)
        
        # We need to translate status into CPC BASIC SOUND command expectations:
        # play_sound signature: (channel_status, period, duration, volume, env, ent, noise)
        self.sound.play_sound(status, period, duration, volume, env, ent, noise)

    def fw_sound_check(self):
        status = 0
        if (self.sound.get_sq_status(1) & 7) == 4: status |= 1 # A free
        if (self.sound.get_sq_status(2) & 7) == 4: status |= 2 # B free
        if (self.sound.get_sq_status(4) & 7) == 4: status |= 4 # C free
        self.z80.A = status
        
    def fw_mc_wait_flyback(self):
        current_time = pygame.time.get_ticks()
        if not hasattr(self, 'last_flyback'):
            self.last_flyback = current_time
            
        wait_time = 20 - (current_time - self.last_flyback)
        if wait_time > 0:
            pygame.time.wait(wait_time)
            
        self.display.update()
        self.last_flyback = pygame.time.get_ticks()

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

    def trigger_error(self, code, line_num):
        self.err_code = code
        self.err_line = line_num
        raise BasicErrorInterrupt()

    def typecast(self, var_name, val):
        if var_name.endswith('%'):
            try: return int(val)
            except: return 0
        elif var_name.endswith('!'):
            try: return float(val)
            except: return 0.0
        elif var_name.endswith('$'):
            return str(val)
        else:
            def_type = self.default_types.get(var_name[0].upper(), 'REAL')
            if def_type == 'INT':
                try: return int(val)
                except: return 0
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
                            if kw in ("RND", "TIME", "XPOS", "YPOS", "VPOS", "INKEY", "ERR", "ERL"):
                                next_idx = i + 2 if skip_next else i + 1
                                if next_idx >= len(expr.tokens) or expr.tokens[next_idx].value != '(':
                                    s += "()"
                        elif t.value in self.arrays and (i + 2 if skip_next else i + 1) < len(expr.tokens) and expr.tokens[(i + 2 if skip_next else i + 1)].value == '(':
                            s += t.value.replace('%', '_PCT').replace('$', '_DLR').replace('!', '_EXC')
                        elif val_upper in self.user_functions:
                            safe_fn = val_upper.replace('%', '_PCT').replace('$', '_DLR').replace('!', '_EXC')
                            s += f"USER_FN_{safe_fn}"
                            # If called without parenthesis, add them
                            next_idx = i + 2 if skip_next else i + 1
                            if next_idx >= len(expr.tokens) or expr.tokens[next_idx].value != '(':
                                s += "()"
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
                            if kw in ("RND", "TIME", "XPOS", "YPOS", "VPOS", "INKEY", "JOY", "PEEK", "LEN", "ERR", "ERL", "EOF"):
                                if i + 1 >= len(expr.tokens) or expr.tokens[i+1].value != '(':
                                    s += "()"
                        else: s += f' {kw} '
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
                            return node
                            
                    tree = ast.parse(s, mode='eval')
                    tree = BitwiseTransformer().visit(tree)
                    ast.fix_missing_locations(tree)
                    code_obj = compile(tree, '<basic_expr>', 'eval')
                    expr._cached_code = code_obj
                except Exception as e:
                    print(f"Error compiling '{s}': {e}")
                    return 0

            try:
                class ArrayWrapper:
                    def __init__(self, arr_dict, is_string):
                        self.arr_dict = arr_dict
                        self.is_string = is_string
                    def __call__(self, *args):
                        return self.arr_dict.get(tuple(int(a) for a in args), "" if self.is_string else 0)
                
                eval_globals = self.builtins.copy()
                def get_var_or_reg(name):
                    if name.startswith('_REG_'):
                        return getattr(self.z80, name[5:], 0)
                    return self.variables.get(name, self.get_default_value(name))
                eval_globals['GET_VAR'] = get_var_or_reg
                eval_globals['GET_INKEY_STR'] = lambda: self.display.get_inkey_str()
                
                for arr_name, arr_dict in self.arrays.items():
                    safe_name = arr_name.replace('%', '_PCT').replace('$', '_DLR').replace('!', '_EXC')
                    eval_globals[safe_name] = ArrayWrapper(arr_dict, arr_name.endswith('$'))
                for fn_name, fn_func in self.user_functions.items():
                    safe_fn = fn_name.replace('%', '_PCT').replace('$', '_DLR').replace('!', '_EXC')
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
            self.stmts_since_event += 1
            
            if is_real_speed:
                self.stmts_this_frame += 1
                if self.stmts_this_frame > statements_limit:
                    current_t = pygame.time.get_ticks() if 'pygame' in sys.modules else 0
                    wait_time = 20 - (current_t - getattr(self, 'last_update', 0))
                    if wait_time > 0 and 'pygame' in sys.modules:
                        pygame.time.wait(wait_time)
                    self.stmts_this_frame = 0
                    self.stmts_since_event = 100 # force event check

            if self.stmts_since_event >= 100:
                current_time = pygame.time.get_ticks() if 'pygame' in sys.modules else 0
                self.last_time = current_time
                if hasattr(self, 'display'):
                    self.display.process_events()
                    if current_time - getattr(self, 'last_update', 0) >= 20:
                        self.display.update()
                        self.last_update = current_time
                        self.stmts_this_frame = 0
                self.stmts_since_event = 0
            else:
                current_time = self.last_time

            # -- Keyboard Interrupt Check (ON BREAK) --
            if hasattr(self, 'display') and getattr(self.display, 'esc_pressed', False):
                self.display.esc_pressed = False
                action = getattr(self, 'on_break_action', 'CONT')
                if action == 'GOSUB' and hasattr(self, 'on_break_line'):
                    self.gosub_stack.append((self.pc, getattr(self, 'next_stmt_idx', 0), True))
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
            if self.interrupts_enabled:
                if hasattr(self, 'sq_timers'):
                    for channel, target in list(self.sq_timers.items()):
                        status = self.sound.get_sq_status(channel)
                        if (status & 7) > 0:
                            self.gosub_stack.append((self.pc, True))
                            self.pc = target
                            self.interrupts_enabled = False
                            del self.sq_timers[channel]
                            interrupt_triggered = True
                            break
                            
                if not interrupt_triggered:
                    for t_id in range(4):
                        t_info = self.timers.get(t_id)
                        if t_info and current_time >= t_info['next_trigger']:
                            # Trigger interrupt: save current PC, jump to target line
                            self.gosub_stack.append((self.pc, True))
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
                
            statements = list(self.program.lines.get(self.pc, []))
            next_pc = self.get_next_line(self.pc)
            
            stmt_idx = getattr(self, 'next_stmt_idx', 0)
            self.next_stmt_idx = 0
            try:
                while stmt_idx < len(statements):
                    self._current_stmt_idx = stmt_idx

                    stmt = statements[stmt_idx]
                    stmt_idx += 1
                    if isinstance(stmt, PrintStatement):
                        out = []
                        newline = True
                        current_using_fmt = None
                        current_vals_for_using = []
                    
                        def flush_using():
                            if current_using_fmt is not None and current_vals_for_using:
                                fmt = str(self.evaluate(current_using_fmt))
                                out.append(format_cpc_using(current_vals_for_using, fmt))
                                current_vals_for_using.clear()

                        for expr in stmt.expressions:
                            if isinstance(expr, Literal) and expr.type == 'USING_FMT':
                                flush_using()
                                current_using_fmt = expr.value
                                continue
                            elif isinstance(expr, Literal) and expr.type == 'SEPARATOR':
                                if expr.value == ';':
                                    newline = False
                                elif expr.value == ',':
                                    flush_using()
                                    out.append('\t')
                                    newline = False
                            else:
                                evaluated = self.evaluate(expr)
                                if current_using_fmt is not None:
                                    current_vals_for_using.append(evaluated)
                                else:
                                    if isinstance(evaluated, float) and evaluated.is_integer():
                                        val = str(int(evaluated))
                                    else:
                                        val = str(evaluated)
                                    if isinstance(evaluated, (int, float)) and evaluated >= 0:
                                        val = " " + val
                                    out.append(val)
                                newline = True
                            
                        flush_using()
                        out_str = "".join(out)
                        
                        # Print to terminal for logging
                        try:
                            print(out_str)
                        except UnicodeEncodeError:
                            print(out_str.encode('ascii', 'replace').decode('ascii'))
                        
                        stream = int(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) is not None else 0
                        if stream == 9 and hasattr(self, 'file_out') and 9 in self.file_out:
                            self.file_out[9].write(out_str + ("\n" if newline else ""))
                        else:
                            # Print to CPC graphical screen
                            if getattr(stmt, 'stream', None) is not None and getattr(stmt, 'stream', None) == 8:
                                self.display.print_text(out_str + ("\r\n" if newline else ""), 0)
                            else:
                                self.display.print_text(out_str + ("\r\n" if newline else ""), stream)

                    elif isinstance(stmt, WriteStatement):
                        out = []
                        for expr in stmt.expressions:
                            if isinstance(expr, Literal) and expr.type == 'SEPARATOR':
                                continue
                            val = self.evaluate(expr)
                            if isinstance(val, str):
                                out.append(f'"{val}"')
                            else:
                                out.append(str(val))
                        out_str = ",".join(out)
                        stream = int(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) is not None else 0
                        if stream == 9 and hasattr(self, 'file_out') and 9 in self.file_out:
                            self.file_out[9].write(out_str + "\n")
                        else:
                            self.display.print_text(out_str + "\r\n", stream)

                    elif isinstance(stmt, LocateStatement):
                        col = int(self.evaluate(stmt.col))
                        row = int(self.evaluate(stmt.row)) if getattr(stmt, 'row', None) else None
                        stream = int(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) else 0
                        if row is not None:
                            self.display.locate(col, row, stream)
                        else:
                            self.display.locate(col, self.display.streams[stream]['text_row'] if hasattr(self.display, 'streams') else self.display.text_row, stream)
                    
                    elif isinstance(stmt, ClsStatement):
                        stream = int(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) else 0
                        self.display.clear_graphics(stream)
                        self.display.locate(1, 1, stream)

                    elif isinstance(stmt, ClgStatement):
                        if hasattr(self.display, 'clear_graphics_window'):
                            self.display.clear_graphics_window()
                        else:
                            self.display.clear_graphics()

                    elif isinstance(stmt, BorderStatement):
                        col1 = int(self.evaluate(stmt.color1))
                        col2 = int(self.evaluate(stmt.color2)) if stmt.color2 else None
                        if hasattr(self.display, 'set_border'):
                            self.display.set_border(col1, col2)

                    elif isinstance(stmt, ClearStatement):
                        self.variables.clear()
                        self.arrays.clear()
                        self.gosub_stack.clear()

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
                        self.tag_active = True
                        if hasattr(self.display, 'tag_active'):
                            self.display.tag_active = True

                    elif isinstance(stmt, TagoffStatement):
                        self.tag_active = False
                        if hasattr(self.display, 'tag_active'):
                            self.display.tag_active = False

                    elif isinstance(stmt, (ZoneStatement, SpeedStatement)):
                        pass # Stubbed to prevent execution errors

                    elif isinstance(stmt, MaskStatement):
                        if stmt.mask is not None:
                            mask = int(self.evaluate(stmt.mask))
                            self.display.set_mask(mask)
                        if stmt.first_point is not None:
                            first_point = int(self.evaluate(stmt.first_point))
                            self.display.set_mask_first(first_point)

                    elif isinstance(stmt, EraseStatement):
                        for var_name in stmt.arrays:
                            if var_name in self.arrays:
                                del self.arrays[var_name]

                    elif isinstance(stmt, AfterStatement):
                        delay = int(self.evaluate(stmt.delay))
                        timer_id = int(self.evaluate(stmt.timer_id))
                        target = int(self.evaluate(stmt.line_number))
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
                        delay = int(self.evaluate(stmt.ticks))
                        timer_id = int(self.evaluate(stmt.timer_id))
                        target = int(self.evaluate(stmt.line_number))
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
                            start = int(self.evaluate(stmt.dims[1]))
                            if len(stmt.dims) >= 3:
                                length = int(self.evaluate(stmt.dims[2]))
                            else:
                                length = len(val)
                        
                            replace_str = val[:length]
                            new_str = var_val[:start-1] + replace_str + var_val[start-1+len(replace_str):]
                            if len(new_str) > len(var_val):
                                new_str = new_str[:len(var_val)]
                        
                            self.variables[target_var] = new_str
                        else:
                            val = self.evaluate(stmt.expr)
                            dims_eval = tuple(int(self.evaluate(d)) for d in stmt.dims)
                            if stmt.var_name not in self.arrays:
                                self.arrays[stmt.var_name] = {}
                            self.arrays[stmt.var_name][dims_eval] = self.typecast(stmt.var_name, val)

                    elif isinstance(stmt, LetStatement):
                        val = self.evaluate(stmt.expr)
                        if stmt.identifier.startswith('_REG_'):
                            setattr(self.z80, stmt.identifier[5:], int(val))
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
                            self.while_stack.append(self.pc)
                        else:
                            depth = 1
                            found = False
                            idx = self.line_numbers.index(self.pc)
                            started = False
                            while idx < len(self.line_numbers):
                                line = self.line_numbers[idx]
                                for s in self.program.lines[line]:
                                    if s is stmt:
                                        started = True
                                        continue
                                    if not started: continue
                                    if isinstance(s, WhileStatement): depth += 1
                                    elif isinstance(s, WendStatement):
                                        depth -= 1
                                        if depth == 0:
                                            next_pc = self.get_next_line(line)
                                            found = True
                                            break
                                if found: break
                                idx += 1

                    elif isinstance(stmt, WendStatement):
                        if hasattr(self, 'while_stack') and self.while_stack:
                            loop_pc = self.while_stack.pop()
                            next_pc = loop_pc
                            break

                    elif isinstance(stmt, OnStatement):
                        val = int(self.evaluate(stmt.expr))
                        if 1 <= val <= len(stmt.line_numbers):
                            target = int(self.evaluate(stmt.line_numbers[val - 1]))
                            if target in self.program.lines:
                                if stmt.is_gosub:
                                    self.gosub_stack.append((self.pc, stmt_idx, False))
                                next_pc = target
                                break
                            else:
                                next_pc = self.trigger_error(8, self.pc)
                                break

                    elif isinstance(stmt, OnErrorStatement):
                        self.error_handler_line = int(self.evaluate(stmt.line_number))
                        if self.error_handler_line == 0:
                            self.error_handler_line = 0 # ON ERROR GOTO 0 disables handler
                            
                    elif isinstance(stmt, OnBreakStatement):
                        self.on_break_action = stmt.action
                        if stmt.line_number is not None:
                            self.on_break_line = int(self.evaluate(stmt.line_number))
                    
                    elif isinstance(stmt, OnSqStatement):
                        channel = int(self.evaluate(stmt.channel)) if stmt.channel else 1
                        target_line = int(self.evaluate(stmt.line_number))
                        if not hasattr(self, 'sq_timers'):
                            self.sq_timers = {}
                        if target_line == 0:
                            if channel in self.sq_timers:
                                del self.sq_timers[channel]
                        else:
                            self.sq_timers[channel] = target_line

                    elif isinstance(stmt, ErrorStatement):
                        code = int(self.evaluate(stmt.code))
                        next_pc = self.trigger_error(code, self.pc)
                        break
                    
                    elif isinstance(stmt, ResumeStatement):
                        if stmt.is_next:
                            next_pc = self.get_next_line(self.pc)
                        elif stmt.line_number is not None:
                            next_pc = int(self.evaluate(stmt.line_number))
                        else:
                            next_pc = self.err_line if self.err_line else self.pc
                        break
                    
                    elif isinstance(stmt, CallStatement):
                        addr = self.evaluate(stmt.address)
                        if isinstance(addr, str) and addr.startswith('0x'):
                            addr = int(addr, 16)
                        elif isinstance(addr, str) and addr.upper().startswith('&BB'):
                            addr = int(addr[1:], 16)
                        else:
                            try: addr = int(addr)
                            except: addr = 0
                        if addr in self.firmware_hooks:
                            self.firmware_hooks[addr]()
                        else:
                            print(f"Warning: Unimplemented CALL &{addr:04X}")

                    elif isinstance(stmt, GotoStatement):
                        target = int(self.evaluate(stmt.line_number))
                        if target in self.program.lines:
                            next_pc = target
                            break
                        else:
                            self.trigger_error(8, self.pc)
                            break
                        
                    elif isinstance(stmt, GosubStatement):
                        target = int(self.evaluate(stmt.line_number))
                        if target in self.program.lines:
                            self.gosub_stack.append((self.pc, stmt_idx, False))
                            next_pc = target
                            break
                        else:
                            self.trigger_error(8, self.pc)
                            break
                        
                    elif isinstance(stmt, ReturnStatement):
                        if self.gosub_stack:
                            ret_val = self.gosub_stack.pop()
                            if isinstance(ret_val, tuple):
                                if len(ret_val) == 3:
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
                        if hasattr(self, 'display'):
                            self.display.print_text(f"SAVE '{filename}' - Use IDE Editor to save\r\n")

                    elif isinstance(stmt, LoadStatement):
                        filename = str(self.evaluate(stmt.filename))
                        if hasattr(self, 'display'):
                            self.display.print_text(f"LOAD '{filename}' - Use IDE Editor to load\r\n")

                    elif isinstance(stmt, EndStatement):
                        self.running = False
                        break
                        
                    elif isinstance(stmt, ModeStatement):
                        mode = int(self.evaluate(stmt.mode_expr))
                        print(f"[VIDEO] Setting MODE {mode}")
                        self.display.set_mode(mode)
                    
                    elif isinstance(stmt, OutStatement):
                        port = int(self.evaluate(stmt.port))
                        value = int(self.evaluate(stmt.value))
                        # CPC hardware out stub
                        pass

                    elif isinstance(stmt, WaitStatement):
                        port = int(self.evaluate(stmt.port))
                        mask = int(self.evaluate(stmt.mask))
                        invert = int(self.evaluate(stmt.invert)) if getattr(stmt, 'invert', None) is not None else 0
                        # stub wait

                    elif isinstance(stmt, CursorStatement):
                        s1 = int(self.evaluate(stmt.switch))
                        s2 = int(self.evaluate(stmt.switch2)) if getattr(stmt, 'switch2', None) is not None else None
                        if hasattr(self.display, 'set_cursor'):
                            self.display.set_cursor(s1, s2)

                    elif isinstance(stmt, PlotrStatement):
                        x = int(self.evaluate(stmt.x))
                        y = int(self.evaluate(stmt.y))
                        pen = int(self.evaluate(stmt.pen)) if getattr(stmt, 'pen', None) is not None else None
                        curr_x = getattr(self.display, 'graphics_x', 0)
                        curr_y = getattr(self.display, 'graphics_y', 0)
                        self.display.plot(curr_x + x, curr_y + y, pen)

                    elif isinstance(stmt, WidthStatement):
                        w = int(self.evaluate(stmt.width))
                        # stub width

                    elif isinstance(stmt, WindowSwapStatement):
                        s1 = int(self.evaluate(stmt.stream1))
                        s2 = int(self.evaluate(stmt.stream2))
                        if hasattr(self.display, 'streams'):
                            tmp = self.display.streams.get(s1, {})
                            self.display.streams[s1] = self.display.streams.get(s2, {})
                            self.display.streams[s2] = tmp

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
                        self.display.print(f"Memory bounds set to {addr}\r\n")

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
                        x = int(self.evaluate(stmt.x))
                        y = int(self.evaluate(stmt.y))
                        pen = int(self.evaluate(stmt.pen)) if stmt.pen else None
                        self.display.plot(x, y, pen)

                    elif isinstance(stmt, DrawStatement):
                        x = int(self.evaluate(stmt.x))
                        y = int(self.evaluate(stmt.y))
                        pen = None
                        if stmt.pen:
                            pen = int(self.evaluate(stmt.pen))
                            self.display.set_graphics_pen(pen)
                        if getattr(stmt, 'mode', None) is not None:
                            mode = int(self.evaluate(stmt.mode))
                            self.display.set_graphics_write_mode(mode)
                        self.display.draw(x, y, pen)

                    elif isinstance(stmt, DrawrStatement):
                        x = int(self.evaluate(stmt.x))
                        y = int(self.evaluate(stmt.y))
                        pen = None
                        if stmt.pen:
                            pen = int(self.evaluate(stmt.pen))
                            self.display.set_graphics_pen(pen)
                        if getattr(stmt, 'mode', None) is not None:
                            mode = int(self.evaluate(stmt.mode))
                            self.display.set_graphics_write_mode(mode)
                        # DRAWR logic: relative to current position
                        curr_x = getattr(self.display, 'graphics_x', 0)
                        curr_y = getattr(self.display, 'graphics_y', 0)
                        self.display.draw(curr_x + x, curr_y + y, pen)

                    elif isinstance(stmt, MoveStatement):
                        x = int(self.evaluate(stmt.x))
                        y = int(self.evaluate(stmt.y))
                        if stmt.pen:
                            pen = int(self.evaluate(stmt.pen))
                            self.display.set_graphics_pen(pen)
                        if stmt.mode is not None:
                            mode = int(self.evaluate(stmt.mode))
                            self.display.set_graphics_write_mode(mode)
                        self.display.move(x, y)

                    elif isinstance(stmt, MoverStatement):
                        x = int(self.evaluate(stmt.x))
                        y = int(self.evaluate(stmt.y))
                        if stmt.pen:
                            pen = int(self.evaluate(stmt.pen))
                            self.display.set_graphics_pen(pen)
                        if getattr(stmt, 'mode', None) is not None:
                            mode = int(self.evaluate(stmt.mode))
                            self.display.set_graphics_write_mode(mode)
                        curr_x = getattr(self.display, 'graphics_x', 0)
                        curr_y = getattr(self.display, 'graphics_y', 0)
                        self.display.move(curr_x + x, curr_y + y)
                    
                    elif isinstance(stmt, OriginStatement):
                        x = int(self.evaluate(stmt.x))
                        y = int(self.evaluate(stmt.y))
                        self.display.origin_x = x
                        self.display.origin_y = y
                        if stmt.left is not None:
                            left = int(self.evaluate(stmt.left))
                            right = int(self.evaluate(stmt.right))
                            top = int(self.evaluate(stmt.top))
                            bottom = int(self.evaluate(stmt.bottom))
                            if hasattr(self.display, 'set_graphics_window'):
                                self.display.set_graphics_window(left, right, top, bottom)

                    elif isinstance(stmt, FillStatement):
                        pen = int(self.evaluate(stmt.pen))
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
                            args = [self.evaluate(p) for p in stmt.params]
                            if len(args) >= 2:
                                err_var = args[0] # Literal string from parse
                                text = str(args[1])
                                if len(args) >= 3:
                                    self.bank_current_record = int(args[2])
                            
                                addr = self.bank_current_record * self.bank_record_length
                                if addr + self.bank_record_length > len(self.bank_memory):
                                    self.variables[err_var] = -1
                                else:
                                    chunk = text.encode('ascii', 'ignore')[:self.bank_record_length]
                                    self.bank_memory[addr:addr+len(chunk)] = chunk
                                    self.variables[err_var] = self.bank_current_record
                                    self.bank_current_record += 1
                        elif stmt.command == 'BANKREAD':
                            # |BANKREAD, @<codigo>, @<cadena> [, <registro>]
                            args = [self.evaluate(p) for p in stmt.params]
                            if len(args) >= 2:
                                err_var = args[0]
                                str_var = args[1]
                                if len(args) >= 3:
                                    self.bank_current_record = int(args[2])
                                
                                addr = self.bank_current_record * self.bank_record_length
                                if addr + self.bank_record_length > len(self.bank_memory):
                                    self.variables[err_var] = -1
                                else:
                                    chunk = self.bank_memory[addr:addr+self.bank_record_length].decode('ascii', 'ignore').rstrip('\x00')
                                    self.variables[str_var] = chunk
                                    self.variables[err_var] = self.bank_current_record
                                    self.bank_current_record += 1
                        elif stmt.command == 'BANKFIND':
                            # |BANKFIND, @<codigo>, <cadena> [, <reg_inicio> [, <reg_fin>]]
                            args = [self.evaluate(p) for p in stmt.params]
                            if len(args) >= 2:
                                err_var = args[0]
                                search = str(args[1])
                                start_reg = self.bank_current_record
                                end_reg = (65536 // self.bank_record_length) - 1
                                if len(args) >= 3:
                                    start_reg = int(args[2])
                                if len(args) >= 4:
                                    end_reg = int(args[3])
                                
                                found = False
                                for r in range(start_reg, end_reg + 1):
                                    addr = r * self.bank_record_length
                                    if addr + self.bank_record_length > len(self.bank_memory):
                                        break
                                    chunk = self.bank_memory[addr:addr+self.bank_record_length].decode('ascii', 'ignore')
                                    # Manual says ? can be used as wildcard in search string!
                                    # "La <cadena buscada> puede contener símbolos comodín, que en este caso son caracteres número 0, chr$(0). El número de caracteres que intervienen en las comparaciones es igual a la <longitud de registro> o a la longitud de la <cadena buscada>, el más corto de los dos."
                                    # Actually, ? is chr$(63). But if the user uses chr$(0) or ? as comodín, we could just do a simple match. Let's do a basic find.
                                    # Wait, the manual says "son caracteres número 0, chr$(0)" but the example says "puede escribir ? como simbolo comodin".
                                    # Let's implement a simple wildcard match
                                    search_len = min(len(search), self.bank_record_length)
                                    match = True
                                    for i in range(search_len):
                                        if search[i] != '\x00' and search[i] != '?' and i < len(chunk) and search[i] != chunk[i]:
                                            match = False
                                            break
                                    if match:
                                        self.variables[err_var] = r
                                        self.bank_current_record = r
                                        found = True
                                        break
                                if not found:
                                    self.variables[err_var] = -3

                    elif isinstance(stmt, InkStatement):
                        pen = int(self.evaluate(stmt.pen))
                        color1 = int(self.evaluate(stmt.color1))
                        color2 = int(self.evaluate(stmt.color2)) if stmt.color2 else None
                        self.display.set_ink(pen, color1, color2)

                    elif isinstance(stmt, PenStatement):
                        if stmt.pen is not None:
                            pen = int(self.evaluate(stmt.pen))
                            stream = int(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) else 0
                            self.display.set_pen(pen, stream)
                        if getattr(stmt, 'bg_mode', None) is not None:
                            bg_mode = int(self.evaluate(stmt.bg_mode))
                            self.display.set_bg_mode(bg_mode)

                    elif isinstance(stmt, PaperStatement):
                        paper = int(self.evaluate(stmt.paper))
                        stream = int(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) else 0
                        self.display.set_paper(paper, stream)
                    
                    elif type(stmt).__name__ == 'GraphicsPenStatement':
                        if stmt.pen is not None:
                            pen = int(self.evaluate(stmt.pen))
                            self.display.set_graphics_pen(pen)
                        if stmt.bg_mode is not None:
                            bg_mode = int(self.evaluate(stmt.bg_mode))
                            self.display.set_bg_mode(bg_mode)

                    elif type(stmt).__name__ == 'GraphicsPaperStatement':
                        paper = int(self.evaluate(stmt.paper))
                        self.display.set_graphics_paper(paper)

                    elif isinstance(stmt, SpeedStatement):
                        if stmt.target == 'INK':
                            if stmt.expr1 is not None:
                                t1 = int(self.evaluate(stmt.expr1))
                                t2 = int(self.evaluate(stmt.expr2)) if stmt.expr2 is not None else t1
                                self.display.set_speed_ink(t1, t2)
                        elif stmt.target == 'KEY':
                            if stmt.expr1 is not None and stmt.expr2 is not None:
                                t1 = int(self.evaluate(stmt.expr1))
                                t2 = int(self.evaluate(stmt.expr2))
                                self.display.set_speed_key(t1, t2)
                        # KEY speed is ignored for now

                    elif isinstance(stmt, EnvStatement):
                        env_no = int(self.evaluate(stmt.env_no))
                        sections = [int(self.evaluate(s)) for s in stmt.sections]
                        self.sound.set_env(env_no, sections)
                    
                    elif isinstance(stmt, EntStatement):
                        ent_no = int(self.evaluate(stmt.ent_no))
                        sections = [int(self.evaluate(s)) for s in stmt.sections]
                        self.sound.set_ent(ent_no, sections)

                    elif isinstance(stmt, SoundStatement):
                        channel = int(self.evaluate(stmt.channel)) if stmt.channel else 1
                        period = int(self.evaluate(stmt.period)) if stmt.period else 0
                        duration = int(self.evaluate(stmt.duration)) if stmt.duration else 20
                        volume = int(self.evaluate(stmt.volume)) if stmt.volume else 12
                        env = int(self.evaluate(stmt.env)) if stmt.env else 0
                        ent = int(self.evaluate(stmt.ent)) if stmt.ent else 0
                        noise = int(self.evaluate(stmt.noise)) if stmt.noise else 0
                        print(f"[AUDIO] SOUND {channel},{period},{duration},{volume}")
                        self.sound.play_sound(channel, period, duration, volume, env, ent, noise)
                    
                    elif isinstance(stmt, ReleaseStatement):
                        channels = int(self.evaluate(stmt.channels))
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
                        self.for_loops[stmt.identifier] = ((self.pc, stmt_idx), end_val, step_val)
                        if stmt.identifier in self.for_stack:
                            self.for_stack.remove(stmt.identifier)
                        self.for_stack.append(stmt.identifier)
                    
                    elif isinstance(stmt, ReadStatement):
                        for var in stmt.variables:
                            if self.data_ptr < len(self.data_values):
                                _, val_expr = self.data_values[self.data_ptr]
                                val = self.evaluate(val_expr)
                                if isinstance(var, tuple):
                                    var_name, dims = var
                                    dims_eval = tuple(int(self.evaluate(d)) for d in dims)
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
                            target_line = int(self.evaluate(stmt.line_number))
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
                        stream = int(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) is not None else 0
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
                                    dims_eval = tuple(int(self.evaluate(d)) for d in dims)
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
                        limit = int(self.evaluate(stmt.limit))
                        if hasattr(self, 'display') and hasattr(self.display, 'symbol_after'):
                            self.display.symbol_after(limit)

                    elif isinstance(stmt, SymbolStatement):
                        char_code = int(self.evaluate(stmt.char_code))
                        matrix = [int(self.evaluate(m)) for m in stmt.matrix]
                        while len(matrix) < 8:
                            matrix.append(0)
                        matrix = matrix[:8]
                        if hasattr(self.display, 'define_symbol'):
                            self.display.define_symbol(char_code, matrix)

                    elif isinstance(stmt, WindowStatement):
                        left = int(self.evaluate(stmt.left))
                        right = int(self.evaluate(stmt.right))
                        top = int(self.evaluate(stmt.top))
                        bottom = int(self.evaluate(stmt.bottom))
                        stream = int(self.evaluate(stmt.stream)) if getattr(stmt, 'stream', None) else 0
                        if hasattr(self.display, 'set_window'):
                            self.display.set_window(left, right, top, bottom, stream)

                    elif isinstance(stmt, PokeStatement):
                        addr = int(self.evaluate(stmt.address)) & 0xFFFF
                        val = int(self.evaluate(stmt.value)) & 0xFF
                        self.ram[addr] = val
                        if addr >= 0xC000:
                            self.display.poke_video_ram(addr, val)
                        
                    elif isinstance(stmt, NextStatement):
                        identifiers = getattr(stmt, 'identifiers', [stmt.identifier])
                    
                        next_jump = None
                        for var_name in identifiers:
                            if not var_name and self.for_stack:
                                var_name = self.for_stack[-1]
                            
                            if var_name in self.for_loops:
                                loop_target, end_val, step_val = self.for_loops[var_name]
                                current_val = self.variables.get(var_name, 0)
                            
                                next_val = current_val + step_val
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


