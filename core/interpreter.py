import math
import random
from core.parser import (Program, PrintStatement, LetStatement, GotoStatement, 
                         ModeStatement, ForStatement, NextStatement, Literal, Variable,
                         PlotStatement, DrawStatement, DrawrStatement, MoveStatement, MoverStatement, InkStatement,
                         PenStatement, PaperStatement, SoundStatement, LocateStatement, 
                         ClsStatement, ClgStatement, RawExpression, IfStatement, GosubStatement, 
                         ReturnStatement, DimStatement, EndStatement, OriginStatement,
                         DataStatement, ReadStatement, RestoreStatement,
                         InputStatement, SymbolStatement, FrameStatement,
                         StopStatement, WindowStatement, WhileStatement, WendStatement,
                         OnStatement)
from video.display import Display
from audio.sound import SoundEngine

def cpc_chr(x): return chr(int(x))
def cpc_asc(x): return ord(x[0]) if x else 0
def cpc_rnd(x=None): return random.random()

class Interpreter:
    def __init__(self, program, scale=2):
        self.program = program
        self.variables = {}
        self.arrays = {}
        self.pc = None
        self.running = False
        self.display = Display(scale=scale)
        self.sound = SoundEngine()
        
        self.line_numbers = sorted(list(self.program.lines.keys()))
        self.for_loops = {}
        self.gosub_stack = []
        self.data_values = []
        self.data_ptr = 0
        
        # Funciones built-in del Amstrad BASIC para el evaluador
        self.builtins = {
            "__builtins__": None,
            "SIN": math.sin,
            "COS": math.cos,
            "TAN": math.tan,
            "INT": int,
            "ABS": abs,
            "RND": cpc_rnd,
            "CHR_STR": cpc_chr,
            "ASC": cpc_asc,
            "SQR": math.sqrt,
            "LOG": math.log,
            "LOG10": math.log10,
            "VAL": lambda x: float(x) if '.' in str(x) else int(x) if str(x).lstrip('-').isdigit() else 0,
            "RIGHT_STR": lambda s, n: s[-n:] if n > 0 else "",
            "MID_STR": lambda s, start, n=None: s[start-1:start-1+n] if n is not None else s[start-1:],
            "LOWER_STR": lambda s: s.lower(),
            "MAX": max,
            "SQ": lambda x: 0,  # stub for sound queue status
            "LEN": len
        }
        
    def get_next_line(self, current_line):
        try:
            idx = self.line_numbers.index(current_line)
            if idx + 1 < len(self.line_numbers):
                return self.line_numbers[idx + 1]
            return None
        except ValueError:
            return None

    def evaluate(self, expr):
        if isinstance(expr, Literal):
            if expr.type == 'NUMBER':
                # very basic float/int distinction
                if '.' in expr.value:
                    return float(expr.value)
                return int(expr.value)
            elif expr.type == 'STRING':
                return expr.value
        elif isinstance(expr, RawExpression):
            s = ""
            for t in expr.tokens:
                if t.type == 'IDENTIFIER':
                    if t.value.upper() == 'INKEY$':
                        inkey_val = self.display.get_inkey_str()
                        s += f'"{inkey_val}"'
                    elif t.value.upper() in ('CHR$', 'LEFT$', 'RIGHT$', 'MID$', 'STR$', 'SPACE$'):
                        s += t.value.upper().replace('$', '_STR')
                    elif t.value.upper() in self.builtins:
                        s += t.value.upper()
                    else:
                        val = self.variables.get(t.value, 0)
                        if isinstance(val, str):
                            s += f'"{val}"'
                        else:
                            s += str(val)
                elif t.type == 'SYMBOL' and t.value == '=':
                    s += '=='
                elif t.type == 'SYMBOL' and t.value == '<>':
                    s += '!='
                elif t.type == 'STRING':
                    s += f'"{t.value}"'
                else:
                    s += str(t.value)
            try:
                return eval(s, self.builtins, {})
            except Exception as e:
                print(f"Error evaluando '{s}': {e}")
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
        
        while self.running and self.pc is not None:
            statements = self.program.lines.get(self.pc, [])
            
            next_pc = self.get_next_line(self.pc)
            
            for stmt in statements:
                if isinstance(stmt, PrintStatement):
                    out = []
                    newline = True
                    for expr in stmt.expressions:
                        if isinstance(expr, Literal) and expr.type == 'SEPARATOR':
                            if expr.value == ';':
                                newline = False
                            elif expr.value == ',':
                                out.append('\t')
                                newline = False
                        else:
                            evaluated = self.evaluate(expr)
                            val = str(evaluated)
                            if isinstance(evaluated, (int, float)) and evaluated >= 0:
                                val = " " + val
                            out.append(val)
                            newline = True
                            
                    out_str = "".join(out)
                    # Print to terminal for logging
                    try:
                        print(out_str)
                    except UnicodeEncodeError:
                        print(out_str.encode('ascii', 'replace').decode('ascii'))
                        
                    # Print to CPC graphical screen
                    self.display.print_text(out_str + ("\n" if newline else ""))
                    
                elif isinstance(stmt, LocateStatement):
                    col = int(self.evaluate(stmt.col))
                    row = int(self.evaluate(stmt.row))
                    self.display.locate(col, row)
                    
                elif isinstance(stmt, ClsStatement):
                    self.display.clear_graphics()
                    self.display.locate(1, 1)

                elif isinstance(stmt, ClgStatement):
                    self.display.clear_graphics()

                elif isinstance(stmt, LetStatement):
                    val = self.evaluate(stmt.expr)
                    self.variables[stmt.identifier] = val
                    
                elif isinstance(stmt, DimStatement):
                    # For simplicity, we just initialize a flat dict/list placeholder
                    # CPC Basic supports multi-dimensional arrays, we'll store them flattened or dict-keyed
                    self.arrays[stmt.var_name] = {}
                    
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
                                self.gosub_stack.append(next_pc)
                            next_pc = target
                            break
                        else:
                            print(f"Line {target} does not exist!")
                            self.running = False
                            break

                elif isinstance(stmt, GotoStatement):
                    target = int(self.evaluate(stmt.line_number))
                    if target in self.program.lines:
                        next_pc = target
                        break
                    else:
                        print(f"Line does not exist in {self.pc}")
                        self.running = False
                        break
                        
                elif isinstance(stmt, GosubStatement):
                    target = int(self.evaluate(stmt.line_number))
                    if target in self.program.lines:
                        self.gosub_stack.append(next_pc)
                        next_pc = target
                        break
                    else:
                        print(f"GOSUB Line does not exist in {self.pc}")
                        self.running = False
                        break
                        
                elif isinstance(stmt, ReturnStatement):
                    if self.gosub_stack:
                        next_pc = self.gosub_stack.pop()
                        break
                    else:
                        print(f"RETURN without GOSUB in {self.pc}")
                        self.running = False
                        break
                        
                elif isinstance(stmt, EndStatement):
                    self.running = False
                    break
                        
                elif isinstance(stmt, ModeStatement):
                    mode = int(self.evaluate(stmt.mode_expr))
                    print(f"[VIDEO] Setting MODE {mode}")
                    self.display.set_mode(mode)
                    
                elif isinstance(stmt, PlotStatement):
                    x = int(self.evaluate(stmt.x))
                    y = int(self.evaluate(stmt.y))
                    pen = int(self.evaluate(stmt.pen)) if stmt.pen else None
                    self.display.plot(x, y, pen)

                elif isinstance(stmt, DrawStatement):
                    x = int(self.evaluate(stmt.x))
                    y = int(self.evaluate(stmt.y))
                    pen = int(self.evaluate(stmt.pen)) if stmt.pen else None
                    self.display.draw(x, y, pen)

                elif isinstance(stmt, DrawrStatement):
                    x = int(self.evaluate(stmt.x))
                    y = int(self.evaluate(stmt.y))
                    pen = int(self.evaluate(stmt.pen)) if stmt.pen else None
                    # DRAWR logic: relative to current position
                    curr_x = getattr(self.display, 'graphics_x', 0)
                    curr_y = getattr(self.display, 'graphics_y', 0)
                    self.display.draw(curr_x + x, curr_y + y, pen)

                elif isinstance(stmt, MoveStatement):
                    x = int(self.evaluate(stmt.x))
                    y = int(self.evaluate(stmt.y))
                    self.display.move(x, y)

                elif isinstance(stmt, MoverStatement):
                    x = int(self.evaluate(stmt.x))
                    y = int(self.evaluate(stmt.y))
                    curr_x = getattr(self.display, 'graphics_x', 0)
                    curr_y = getattr(self.display, 'graphics_y', 0)
                    self.display.move(curr_x + x, curr_y + y)
                    
                elif isinstance(stmt, OriginStatement):
                    x = int(self.evaluate(stmt.x))
                    y = int(self.evaluate(stmt.y))
                    self.display.origin_x = x
                    self.display.origin_y = y

                elif isinstance(stmt, InkStatement):
                    pen = int(self.evaluate(stmt.pen))
                    color1 = int(self.evaluate(stmt.color1))
                    self.display.set_ink(pen, color1)

                elif isinstance(stmt, PenStatement):
                    pen = int(self.evaluate(stmt.pen))
                    self.display.set_pen(pen)

                elif isinstance(stmt, PaperStatement):
                    paper = int(self.evaluate(stmt.paper))
                    self.display.set_paper(paper)

                elif isinstance(stmt, SoundStatement):
                    channel = int(self.evaluate(stmt.channel))
                    period = int(self.evaluate(stmt.period))
                    duration = int(self.evaluate(stmt.duration))
                    volume = int(self.evaluate(stmt.volume))
                    env = int(self.evaluate(stmt.env))
                    ent = int(self.evaluate(stmt.ent))
                    noise = int(self.evaluate(stmt.noise))
                    print(f"[AUDIO] SOUND {channel},{period},{duration},{volume}")
                    self.sound.play_sound(channel, period, duration, volume, env, ent, noise)
                    
                elif isinstance(stmt, IfStatement):
                    cond_val = self.evaluate(stmt.condition)
                    if cond_val:
                        if isinstance(stmt.then_stmt, GotoStatement):
                            target = self.evaluate(stmt.then_stmt.line_number)
                            if target in self.program.lines:
                                next_pc = target
                                break
                            else:
                                print(f"Line {target} does not exist!")
                                self.running = False
                                break
                        else:
                            # Execute inline statement
                            statements.append(stmt.then_stmt) # It will be processed in the next loop iteration of this same line
                            
                elif isinstance(stmt, ForStatement):
                    start_val = self.evaluate(stmt.start_expr)
                    end_val = self.evaluate(stmt.end_expr)
                    step_val = self.evaluate(stmt.step_expr)
                    
                    self.variables[stmt.identifier] = start_val
                    self.for_loops[stmt.identifier] = (next_pc, end_val, step_val)
                    
                elif isinstance(stmt, ReadStatement):
                    for var in stmt.variables:
                        if self.data_ptr < len(self.data_values):
                            _, val_expr = self.data_values[self.data_ptr]
                            val = self.evaluate(val_expr)
                            self.variables[var] = val
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

                elif isinstance(stmt, StopStatement):
                    print("STOP at line", self.pc)
                    self.running = False
                    break

                elif isinstance(stmt, InputStatement):
                    if stmt.prompt:
                        self.display.print_text(stmt.prompt)
                        self.display.update()
                    # We use the new pygame input method
                    val = self.display.input_string()
                    print(f"[INPUT] user entered: {val}")
                    if stmt.variables:
                        var = stmt.variables[0]
                        if not var.endswith('$'):
                            try:
                                val = float(val) if '.' in val else int(val)
                            except ValueError:
                                val = 0
                        self.variables[var] = val

                elif isinstance(stmt, FrameStatement):
                    import pygame
                    pygame.time.wait(20)

                elif isinstance(stmt, SymbolStatement):
                    char_code = self.evaluate(stmt.char_code)
                    matrix = [self.evaluate(m) for m in stmt.matrix]
                    print(f"SYMBOL {char_code} defined with matrix {matrix}")

                elif isinstance(stmt, WindowStatement):
                    left = self.evaluate(stmt.left)
                    right = self.evaluate(stmt.right)
                    top = self.evaluate(stmt.top)
                    bottom = self.evaluate(stmt.bottom)
                    print(f"WINDOW defined: {left},{right},{top},{bottom}")
                        
                elif isinstance(stmt, NextStatement):
                    if stmt.identifier in self.for_loops:
                        loop_target, end_val, step_val = self.for_loops[stmt.identifier]
                        current_val = self.variables.get(stmt.identifier, 0)
                        
                        next_val = current_val + step_val
                        self.variables[stmt.identifier] = next_val
                        
                        if (step_val > 0 and next_val <= end_val) or (step_val < 0 and next_val >= end_val):
                            next_pc = loop_target
                            break
                        else:
                            del self.for_loops[stmt.identifier]
            
            self.display.update()
            self.display.process_events()
            
            self.pc = next_pc
        
        # Keep window open
        while True:
            self.display.process_events()
            self.display.update()

