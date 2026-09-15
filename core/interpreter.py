import math
import random
from core.parser import (Program, PrintStatement, LetStatement, GotoStatement, 
                         ModeStatement, ForStatement, NextStatement, Literal, Variable,
                         PlotStatement, DrawStatement, MoveStatement, InkStatement,
                         PenStatement, PaperStatement, SoundStatement, LocateStatement, 
                         ClsStatement, RawExpression, IfStatement, GosubStatement, 
                         ReturnStatement, DimStatement, EndStatement)
from video.display import Display
from audio.sound import SoundEngine

def cpc_chr(x): return chr(int(x))
def cpc_asc(x): return ord(x[0]) if x else 0
def cpc_rnd(): return random.random()

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
            "LOG10": math.log10
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

    def execute(self):
        if not self.line_numbers:
            return
            
        self.pc = self.line_numbers[0]
        self.running = True
        
        while self.running and self.pc is not None:
            statements = self.program.lines.get(self.pc, [])
            
            next_pc = self.get_next_line(self.pc)
            
            for stmt in statements:
                if isinstance(stmt, PrintStatement):
                    out = []
                    for expr in stmt.expressions:
                        out.append(str(self.evaluate(expr)))
                    # Print to terminal for logging
                    print(" ".join(out))
                    # Print to CPC graphical screen (with a newline at the end)
                    self.display.print_text(" ".join(out) + "\n")
                    
                elif isinstance(stmt, LocateStatement):
                    col = int(self.evaluate(stmt.col))
                    row = int(self.evaluate(stmt.row))
                    self.display.locate(col, row)
                    
                elif isinstance(stmt, ClsStatement):
                    self.display.clear_graphics()
                    self.display.locate(1, 1)

                elif isinstance(stmt, LetStatement):
                    val = self.evaluate(stmt.expr)
                    self.variables[stmt.identifier] = val
                    
                elif isinstance(stmt, DimStatement):
                    # For simplicity, we just initialize a flat dict/list placeholder
                    # CPC Basic supports multi-dimensional arrays, we'll store them flattened or dict-keyed
                    self.arrays[stmt.var_name] = {}
                    
                elif isinstance(stmt, GotoStatement):
                    target = self.evaluate(stmt.line_number)
                    if target in self.program.lines:
                        next_pc = target
                        break
                    else:
                        print(f"Line does not exist in {self.pc}")
                        self.running = False
                        break
                        
                elif isinstance(stmt, GosubStatement):
                    target = self.evaluate(stmt.line_number)
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

                elif isinstance(stmt, MoveStatement):
                    x = int(self.evaluate(stmt.x))
                    y = int(self.evaluate(stmt.y))
                    self.display.move(x, y)

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

