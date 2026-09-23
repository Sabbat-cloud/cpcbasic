from core.lexer import Lexer, EOF, NUMBER, HEX_NUMBER, STRING, IDENTIFIER, KEYWORD, SYMBOL, NEWLINE
from core.lexer import Token

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, lines):
        # Dictionary mapping line number (int) to a list of statements
        self.lines = lines

class Statement(ASTNode):
    pass

class BorderStatement(Statement):
    def __init__(self, color1, color2=None):
        self.color1 = color1
        self.color2 = color2

class ClearStatement(Statement):
    pass

class ClearInputStatement(Statement):
    pass

class RandomizeStatement(Statement):
    def __init__(self, expr=None):
        self.expr = expr

class DegStatement(Statement):
    pass

class RadStatement(Statement):
    pass

class EnvStatement(Statement):
    def __init__(self, env_no, sections):
        self.env_no = env_no
        self.sections = sections

class EntStatement(Statement):
    def __init__(self, ent_no, sections):
        self.ent_no = ent_no
        self.sections = sections

class FillStatement(Statement):
    def __init__(self, pen):
        self.pen = pen

class DataStatement(Statement):
    def __init__(self, values):
        self.values = values

class ReadStatement(Statement):
    def __init__(self, variables):
        self.variables = variables

class RestoreStatement(Statement):
    def __init__(self, line_number=None):
        self.line_number = line_number

class DefTypeStatement(Statement):
    def __init__(self, type_name, ranges):
        self.type_name = type_name
        self.ranges = ranges

class DefFnStatement(Statement):
    def __init__(self, name, params, expr):
        self.name = name
        self.params = params
        self.expr = expr

class InputStatement(Statement):
    def __init__(self, prompt, variables, stream=0):
        self.prompt = prompt
        self.variables = variables
        self.stream = stream

class SymbolStatement(Statement):
    def __init__(self, char_code, matrix):
        self.char_code = char_code
        self.matrix = matrix

class FrameStatement(Statement):
    pass

class StopStatement(Statement):
    pass

class DiStatement(Statement):
    pass

class EiStatement(Statement):
    pass

class WindowStatement(Statement):
    def __init__(self, left, right, top, bottom, stream=None):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.stream = stream

class WhileStatement(Statement):
    def __init__(self, condition):
        self.condition = condition

class WendStatement(Statement):
    pass

class OnStatement(Statement):
    def __init__(self, expr, is_gosub, line_numbers):
        self.expr = expr
        self.is_gosub = is_gosub
        self.line_numbers = line_numbers

class AfterStatement(Statement):
    def __init__(self, delay, timer_id, line_number):
        self.delay = delay
        self.timer_id = timer_id
        self.line_number = line_number

class EveryStatement(Statement):
    def __init__(self, delay, timer_id, line_number):
        self.delay = delay
        self.timer_id = timer_id
        self.line_number = line_number

class OnBreakStatement(Statement):
    def __init__(self, action, line_number=None):
        self.action = action # 'CONT', 'STOP', 'GOSUB'
        self.line_number = line_number

class MaskStatement(Statement):
    def __init__(self, mask, first_point=None):
        self.mask = mask
        self.first_point = first_point

class CallStatement(Statement):
    def __init__(self, address, params):
        self.address = address
        self.params = params

class RsxStatement(Statement):
    def __init__(self, command, params):
        self.command = command
        self.params = params

class OnErrorStatement(Statement):
    def __init__(self, line_number):
        self.line_number = line_number

class OnSqStatement(Statement):
    def __init__(self, channel, line_number):
        self.channel = channel
        self.line_number = line_number

class ErrorStatement(Statement):
    def __init__(self, code):
        self.code = code

class ResumeStatement(Statement):
    def __init__(self, line_number=None, is_next=False):
        self.line_number = line_number
        self.is_next = is_next

class OpenInStatement(Statement):
    def __init__(self, filename):
        self.filename = filename

class OpenOutStatement(Statement):
    def __init__(self, filename):
        self.filename = filename

class CloseInStatement(Statement):
    pass

class CloseOutStatement(Statement):
    pass

class PokeStatement(Statement):
    def __init__(self, address, value):
        self.address = address
        self.value = value

class TagStatement(Statement):
    pass

class TagoffStatement(Statement):
    pass

class ZoneStatement(Statement):
    def __init__(self, width):
        self.width = width

class SpeedStatement(Statement):
    def __init__(self, type_, params):
        self.type = type_ # 'INK' or 'KEY'
        self.params = params

class PrintStatement(Statement):
    def __init__(self, expressions):
        self.expressions = expressions

class LetStatement(Statement):
    def __init__(self, identifier, expr):
        self.identifier = identifier
        self.expr = expr

class GotoStatement(Statement):
    def __init__(self, line_number):
        self.line_number = line_number
        
class ModeStatement(Statement):
    def __init__(self, mode_expr):
        self.mode_expr = mode_expr
        
class ForStatement(Statement):
    def __init__(self, identifier, start_expr, end_expr, step_expr):
        self.identifier = identifier
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.step_expr = step_expr

class NextStatement(Statement):
    def __init__(self, identifiers):
        self.identifiers = identifiers
        # for backwards compatibility with any remaining code:
        self.identifier = identifiers[0] if identifiers else None

class PlotStatement(Statement):
    def __init__(self, x, y, pen=None):
        self.x = x
        self.y = y
        self.pen = pen

class DrawStatement(Statement):
    def __init__(self, x, y, pen=None, mode=None):
        self.x = x
        self.y = y
        self.pen = pen
        self.mode = mode

class DrawrStatement(Statement):
    def __init__(self, x, y, pen=None, mode=None):
        self.x = x
        self.y = y
        self.pen = pen
        self.mode = mode

class MoveStatement(Statement):
    def __init__(self, x, y, pen=None, mode=None):
        self.x = x
        self.y = y
        self.pen = pen
        self.mode = mode

class MoverStatement(Statement):
    def __init__(self, x, y, pen=None, mode=None):
        self.x = x
        self.y = y
        self.pen = pen
        self.mode = mode

class OriginStatement(Statement):
    def __init__(self, x, y, left=None, right=None, top=None, bottom=None):
        self.x = x
        self.y = y
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

class InkStatement(Statement):
    def __init__(self, pen, color1, color2=None):
        self.pen = pen
        self.color1 = color1
        self.color2 = color2

class PenStatement(Statement):
    def __init__(self, pen, bg_mode=None, stream=None):
        self.pen = pen
        self.bg_mode = bg_mode
        self.stream = stream
        
class PaperStatement(Statement):
    def __init__(self, paper, stream=None):
        self.paper = paper
        self.stream = stream

class GraphicsPenStatement(Statement):
    def __init__(self, pen, bg_mode=None):
        self.pen = pen
        self.bg_mode = bg_mode

class GraphicsPaperStatement(Statement):
    def __init__(self, paper):
        self.paper = paper

class LocateStatement(Statement):
    def __init__(self, col, row, stream=None):
        self.col = col
        self.row = row
        self.stream = stream

class ClsStatement(Statement):
    def __init__(self, stream=None):
        self.stream = stream

class ClgStatement(Statement):
    pass

class IfStatement(Statement):
    def __init__(self, condition, then_stmts, else_stmts=None):
        self.condition = condition
        self.then_stmts = then_stmts
        self.else_stmts = else_stmts or []

class GosubStatement(Statement):
    def __init__(self, line_number):
        self.line_number = line_number

class ReturnStatement(Statement):
    pass

class EraseStatement(Statement):
    def __init__(self, arrays):
        self.arrays = arrays

class EveryStatement(Statement):
    def __init__(self, ticks, timer_id, line_number):
        self.ticks = ticks
        self.timer_id = timer_id
        self.line_number = line_number
        
class LetArrayStatement(Statement):
    def __init__(self, var_name, dims, expr):
        self.var_name = var_name
        self.dims = dims
        self.expr = expr

class DimStatement(Statement):
    def __init__(self, arrays):
        self.arrays = arrays

class EndStatement(Statement):
    pass

class Expr(ASTNode):
    pass

class RawExpression(Expr):
    def __init__(self, tokens):
        self.tokens = tokens

class SoundStatement(Statement):
    def __init__(self, channel, period, duration, volume, env, ent, noise):
        self.channel = channel
        self.period = period
        self.duration = duration
        self.volume = volume
        self.env = env
        self.ent = ent
        self.noise = noise

class Expr(ASTNode):
    pass

class Literal(Expr):
    def __init__(self, value, type_):
        self.value = value
        self.type = type_

    def __repr__(self):
        return f"Literal({self.value}, {self.type})"

class Variable(Expr):
    def __init__(self, name):
        self.name = name

class BinOp(Expr):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            raise Exception(f"Expected {token_type}, got {self.current_token.type} at line {self.current_token.line}")

    def parse(self):
        lines = {}
        
        while self.current_token.type != EOF:
            if self.current_token.type == NEWLINE:
                self.eat(NEWLINE)
                continue
                
            if self.current_token.type == NUMBER:
                line_num = int(self.current_token.value)
                self.eat(NUMBER)
                
                statements = []
                while self.current_token.type != NEWLINE and self.current_token.type != EOF:
                    prev_pos = self.pos
                    stmt = self.parse_statement()
                    if stmt:
                        statements.append(stmt)
                    
                    if self.current_token.type == SYMBOL and self.current_token.value == ':':
                        self.eat(SYMBOL) # Multiple statements on one line
                        
                    if self.pos == prev_pos:
                        # Prevent infinite loop if statement is not recognized
                        self.pos += 1
                        if self.pos < len(self.tokens):
                            self.current_token = self.tokens[self.pos]
                
                lines[line_num] = statements
            else:
                # Command without line number (direct mode) - skip for now or throw error
                # For simplicity, we just eat to EOF or newline
                while self.current_token.type != NEWLINE and self.current_token.type != EOF:
                    self.pos += 1
                    self.current_token = self.tokens[self.pos]
                
        return Program(lines)

    def parse_statement(self):
        if self.current_token.type == KEYWORD:
            if self.current_token.value == 'PRINT':
                self.eat(KEYWORD)
                stream = None
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                
                exprs = []
                while self.current_token.type not in (NEWLINE, EOF) and not (self.current_token.type == SYMBOL and self.current_token.value == ':'):
                    if self.current_token.type == KEYWORD and self.current_token.value == 'USING':
                        self.eat(KEYWORD)
                        exprs.append(Literal(self.parse_expression(), "USING_FMT"))
                        if self.current_token.type == SYMBOL and self.current_token.value == ';':
                            self.eat(SYMBOL)
                    elif self.current_token.type == SYMBOL and self.current_token.value in (';', ','):
                        exprs.append(Literal(self.current_token.value, "SEPARATOR"))
                        self.eat(SYMBOL)
                    else:
                        expr = self.parse_expression()
                        if expr is not None:
                            exprs.append(expr)
                        else:
                            break
                # Monkey-patch stream into PrintStatement for interpreter
                stmt = PrintStatement(exprs)
                stmt.stream = stream
                return stmt
            
            elif self.current_token.value == 'POKE':
                self.eat(KEYWORD)
                addr_expr = self.parse_expression()
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                val_expr = self.parse_expression()
                return PokeStatement(addr_expr, val_expr)

            elif self.current_token.value == 'GOTO':
                self.eat(KEYWORD)
                expr = self.parse_expression()
                return GotoStatement(expr)

            elif self.current_token.value == 'GOSUB':
                self.eat(KEYWORD)
                expr = self.parse_expression()
                return GosubStatement(expr)

            elif self.current_token.value == 'RETURN':
                self.eat(KEYWORD)
                return ReturnStatement()

            elif self.current_token.value == 'ERASE':
                self.eat(KEYWORD)
                arrays = []
                while True:
                    arrays.append(self.current_token.value)
                    self.eat(IDENTIFIER)
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                    else:
                        break
                return EraseStatement(arrays)

            elif self.current_token.value == 'EVERY':
                self.eat(KEYWORD)
                ticks = self.parse_expression()
                timer_id = None
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    timer_id = self.parse_expression()
                if self.current_token.type == KEYWORD and self.current_token.value == 'GOSUB':
                    self.eat(KEYWORD)
                    line_number = self.parse_expression()
                else:
                    raise Exception('Expected GOSUB after EVERY')
                return EveryStatement(ticks, timer_id, line_number)

            elif self.current_token.value == 'DIM':
                self.eat(KEYWORD)
                arrays = []
                while True:
                    var_name = self.current_token.value
                    self.eat(IDENTIFIER)
                    self.eat(SYMBOL) # (
                    dims = []
                    while True:
                        dims.append(self.parse_expression())
                        if self.current_token.type == SYMBOL and self.current_token.value == ',':
                            self.eat(SYMBOL)
                        else:
                            break
                    self.eat(SYMBOL) # )
                    arrays.append((var_name, dims))
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                    else:
                        break
                return DimStatement(arrays)

            elif self.current_token.value == 'END':
                self.eat(KEYWORD)
                return EndStatement()

            elif self.current_token.value == 'DATA':
                self.eat(KEYWORD)
                values = []
                while True:
                    if self.current_token.type in (EOF, NEWLINE) or (self.current_token.type == SYMBOL and self.current_token.value == ':'):
                        break
                    
                    tokens = []
                    while self.current_token.type not in (EOF, NEWLINE) and not (self.current_token.type == SYMBOL and self.current_token.value in (',', ':')):
                        tokens.append(self.current_token)
                        self.pos += 1
                        if self.pos < len(self.tokens):
                            self.current_token = self.tokens[self.pos]
                    
                    if tokens:
                        if len(tokens) == 1 and tokens[0].type == STRING:
                            values.append(Literal(tokens[0].value, STRING))
                        else:
                            # Reconstruct string, preserving spaces using token columns
                            s = ""
                            last_col = -1
                            is_num = True
                            for t in tokens:
                                if last_col != -1 and t.column > last_col:
                                    s += " " * (t.column - last_col)
                                s += str(t.value)
                                last_col = t.column + len(str(t.value))
                                if t.type not in (NUMBER, HEX_NUMBER) and not (t.type == SYMBOL and t.value in ('+', '-', '.')):
                                    is_num = False
                            
                            if is_num:
                                try:
                                    float(s)
                                    values.append(Literal(s, NUMBER))
                                except ValueError:
                                    values.append(Literal(s, STRING))
                            else:
                                values.append(Literal(s, STRING))
                    
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                    else:
                        break
                return DataStatement(values)

            elif self.current_token.value == 'READ':
                self.eat(KEYWORD)
                variables = []
                while True:
                    if self.current_token.type == IDENTIFIER:
                        var_name = self.current_token.value
                        self.eat(IDENTIFIER)
                        if self.current_token.type == SYMBOL and self.current_token.value == '(':
                            self.eat(SYMBOL)
                            dims = []
                            while True:
                                dims.append(self.parse_expression())
                                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                                    self.eat(SYMBOL)
                                else:
                                    break
                            self.eat(SYMBOL) # )
                            variables.append((var_name, dims))
                        else:
                            variables.append(var_name)
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                    else:
                        break
                return ReadStatement(variables)

            elif self.current_token.value == 'RESTORE':
                self.eat(KEYWORD)
                line_number = None
                if self.current_token.type == NUMBER:
                    line_number = self.parse_expression()
                return RestoreStatement(line_number)

            elif self.current_token.value == 'INPUT' or (self.current_token.type == IDENTIFIER and self.current_token.value.upper() == 'LINE' and getattr(self, 'tokens', []) and self.pos + 1 < len(self.tokens) and self.tokens[self.pos+1].value == 'INPUT'):
                if self.current_token.value.upper() == 'LINE':
                    self.eat(IDENTIFIER)
                self.eat(KEYWORD)
                
                stream = Literal("0", NUMBER)
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)

                prompt = None
                if self.current_token.type == STRING:
                    prompt = self.current_token.value
                    self.eat(STRING)
                    if self.current_token.type == SYMBOL and self.current_token.value in (';', ','):
                        self.eat(SYMBOL)
                variables = []
                while True:
                    if self.current_token.type == IDENTIFIER:
                        variables.append(self.current_token.value)
                        self.eat(IDENTIFIER)
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                    else:
                        break
                return InputStatement(prompt, variables, stream)

            elif self.current_token.value == 'FRAME':
                self.eat(KEYWORD)
                return FrameStatement()

            elif self.current_token.value == 'STOP':
                self.eat(KEYWORD)
                return StopStatement()

            elif self.current_token.value == 'SYMBOL':
                self.eat(KEYWORD)
                char_code = self.parse_expression()
                self.eat(SYMBOL) # ,
                matrix = []
                while True:
                    matrix.append(self.parse_expression())
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                    else:
                        break
                return SymbolStatement(char_code, matrix)

            elif self.current_token.value == 'WINDOW':
                self.eat(KEYWORD)
                stream = None
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                left = self.parse_expression()
                self.eat(SYMBOL)
                right = self.parse_expression()
                self.eat(SYMBOL)
                top = self.parse_expression()
                self.eat(SYMBOL)
                bottom = self.parse_expression()
                return WindowStatement(left, right, top, bottom, stream)

            elif self.current_token.value == 'IF':
                self.eat(KEYWORD)
                condition = self.parse_expression()
                if self.current_token.type == KEYWORD and self.current_token.value == 'THEN':
                    self.eat(KEYWORD)
                
                then_stmts = []
                else_stmts = []
                
                # Parse THEN branch
                if self.current_token.type == NUMBER:
                    line_num = self.parse_expression()
                    then_stmts.append(GotoStatement(line_num))
                else:
                    while self.current_token.type not in (NEWLINE, EOF) and not (self.current_token.type == KEYWORD and self.current_token.value == 'ELSE'):
                        prev_pos = self.pos
                        stmt = self.parse_statement()
                        if stmt:
                            then_stmts.append(stmt)
                        if self.current_token.type == SYMBOL and self.current_token.value == ':':
                            self.eat(SYMBOL)
                        if self.pos == prev_pos:
                            self.pos += 1
                            if self.pos < len(self.tokens):
                                self.current_token = self.tokens[self.pos]
                            
                # Parse ELSE branch
                if self.current_token.type == KEYWORD and self.current_token.value == 'ELSE':
                    self.eat(KEYWORD)
                    if self.current_token.type == NUMBER:
                        line_num = self.parse_expression()
                        else_stmts.append(GotoStatement(line_num))
                    else:
                        while self.current_token.type not in (NEWLINE, EOF):
                            prev_pos = self.pos
                            stmt = self.parse_statement()
                            if stmt:
                                else_stmts.append(stmt)
                            if self.current_token.type == SYMBOL and self.current_token.value == ':':
                                self.eat(SYMBOL)
                            if self.pos == prev_pos:
                                self.pos += 1
                                if self.pos < len(self.tokens):
                                    self.current_token = self.tokens[self.pos]
                
                return IfStatement(condition, then_stmts, else_stmts)

            elif self.current_token.value == 'WHILE':
                self.eat(KEYWORD)
                condition = self.parse_expression()
                return WhileStatement(condition)

            elif self.current_token.value == 'WEND':
                self.eat(KEYWORD)
                return WendStatement()

            elif self.current_token.value in ('AFTER', 'EVERY'):
                is_after = self.current_token.value == 'AFTER'
                self.eat(KEYWORD)
                delay = self.parse_expression()
                timer_id = Literal("0", NUMBER)
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    timer_id = self.parse_expression()
                # next token should be GOSUB, but if it's multiple statements maybe not?
                # The manual says AFTER <delay>[, <timer_id>] GOSUB <line>
                if self.current_token.type == KEYWORD and self.current_token.value == 'GOSUB':
                    self.eat(KEYWORD)
                line_number = self.parse_expression()
                if is_after:
                    return AfterStatement(delay, timer_id, line_number)
                else:
                    return EveryStatement(delay, timer_id, line_number)

            elif self.current_token.value == 'ON':
                self.eat(KEYWORD)
                if self.current_token.type == KEYWORD and self.current_token.value == 'BREAK':
                    self.eat(KEYWORD)
                    action = self.current_token.value # CONT, STOP, GOSUB
                    self.eat(KEYWORD)
                    line_number = None
                    if action == 'GOSUB':
                        line_number = self.parse_expression()
                    return OnBreakStatement(action, line_number)
                    
                if self.current_token.type == KEYWORD and self.current_token.value == 'ERROR':
                    self.eat(KEYWORD)
                    if self.current_token.type == KEYWORD and self.current_token.value == 'GOTO':
                        self.eat(KEYWORD)
                    line_number = self.parse_expression()
                    return OnErrorStatement(line_number)
                
                if self.current_token.type == KEYWORD and self.current_token.value == 'SQ':
                    self.eat(KEYWORD)
                    # parse optional '(' channel ')'
                    channel = None
                    if self.current_token.type == SYMBOL and self.current_token.value == '(':
                        self.eat(SYMBOL)
                        channel = self.parse_expression()
                        if self.current_token.type == SYMBOL and self.current_token.value == ')':
                            self.eat(SYMBOL)
                    else:
                        channel = self.parse_expression()
                    if self.current_token.type == KEYWORD and self.current_token.value == 'GOSUB':
                        self.eat(KEYWORD)
                    line_number = self.parse_expression()
                    return OnSqStatement(channel, line_number)
                    
                expr = self.parse_expression()
                is_gosub = False
                if self.current_token.type == KEYWORD and self.current_token.value == 'GOSUB':
                    self.eat(KEYWORD)
                    is_gosub = True
                elif self.current_token.type == KEYWORD and self.current_token.value == 'GOTO':
                    self.eat(KEYWORD)
                line_numbers = []
                while True:
                    line_numbers.append(self.parse_expression())
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                    else:
                        break
                return OnStatement(expr, is_gosub, line_numbers)

            elif self.current_token.value == 'MASK':
                self.eat(KEYWORD)
                mask = None
                first_point = None
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    first_point = self.parse_expression()
                else:
                    mask = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                        first_point = self.parse_expression()
                return MaskStatement(mask, first_point)

            elif self.current_token.value == 'TAG':
                self.eat(KEYWORD)
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression()
                return TagStatement()

            elif self.current_token.value == 'TAGOFF':
                self.eat(KEYWORD)
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression()
                return TagoffStatement()

            elif self.current_token.value == 'ZONE':
                self.eat(KEYWORD)
                width = self.parse_expression()
                return ZoneStatement(width)

            elif self.current_token.value == 'SPEED':
                self.eat(KEYWORD)
                type_ = self.current_token.value # INK or KEY
                self.eat(KEYWORD)
                params = []
                while True:
                    params.append(self.parse_expression())
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                    else:
                        break
                return SpeedStatement(type_, params)
                
            elif self.current_token.value == 'MODE':
                self.eat(KEYWORD)
                expr = self.parse_expression()
                return ModeStatement(expr)
                
            elif self.current_token.value == 'FOR':
                self.eat(KEYWORD)
                var_name = self.current_token.value
                self.eat(IDENTIFIER)
                if self.current_token.value == '=':
                    self.eat(SYMBOL)
                start_expr = self.parse_expression()
                
                if self.current_token.value == 'TO':
                    self.eat(KEYWORD)
                end_expr = self.parse_expression()
                
                step_expr = Literal("1", NUMBER)
                if self.current_token.type == KEYWORD and self.current_token.value == 'STEP':
                    self.eat(KEYWORD)
                    step_expr = self.parse_expression()
                    
                return ForStatement(var_name, start_expr, end_expr, step_expr)
                
            elif self.current_token.value == 'NEXT':
                self.eat(KEYWORD)
                var_names = []
                while self.current_token.type not in (NEWLINE, EOF) and not (self.current_token.type == SYMBOL and self.current_token.value == ':'):
                    if self.current_token.type == IDENTIFIER:
                        var_names.append(self.current_token.value)
                        self.eat(IDENTIFIER)
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                    else:
                        break
                if not var_names:
                    var_names = [None]
                return NextStatement(var_names)
                
            elif self.current_token.value == 'PLOT':
                self.eat(KEYWORD)
                x = self.parse_expression()
                self.eat(SYMBOL) # ,
                y = self.parse_expression()
                pen = None
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    pen = self.parse_expression()
                return PlotStatement(x, y, pen)
                
            elif self.current_token.value == 'DRAW':
                self.eat(KEYWORD)
                x = self.parse_expression()
                self.eat(SYMBOL) # ,
                y = self.parse_expression()
                pen = None
                mode = None
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    if self.current_token.type != SYMBOL or self.current_token.value != ',':
                        pen = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                        mode = self.parse_expression()
                return DrawStatement(x, y, pen, mode)

            elif self.current_token.value == 'DRAWR':
                self.eat(KEYWORD)
                x = self.parse_expression()
                self.eat(SYMBOL) # ,
                y = self.parse_expression()
                pen = None
                mode = None
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    if self.current_token.type != SYMBOL or self.current_token.value != ',':
                        pen = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                        mode = self.parse_expression()
                return DrawrStatement(x, y, pen, mode)

            elif self.current_token.value == 'MOVE':
                self.eat(KEYWORD)
                x = self.parse_expression()
                self.eat(SYMBOL) # ,
                y = self.parse_expression()
                pen = None
                mode = None
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    if self.current_token.type != SYMBOL or self.current_token.value != ',':
                        pen = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                        mode = self.parse_expression()
                return MoveStatement(x, y, pen, mode)
                
            elif self.current_token.value == 'MOVER':
                self.eat(KEYWORD)
                x = self.parse_expression()
                self.eat(SYMBOL) # ,
                y = self.parse_expression()
                pen = None
                mode = None
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    if self.current_token.type != SYMBOL or self.current_token.value != ',':
                        pen = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                        mode = self.parse_expression()
                return MoverStatement(x, y, pen, mode)

            elif self.current_token.value == 'ORIGIN':
                self.eat(KEYWORD)
                x = self.parse_expression()
                self.eat(SYMBOL) # ,
                y = self.parse_expression()
                left = right = top = bottom = None
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    left = self.parse_expression()
                    self.eat(SYMBOL)
                    right = self.parse_expression()
                    self.eat(SYMBOL)
                    top = self.parse_expression()
                    self.eat(SYMBOL)
                    bottom = self.parse_expression()
                return OriginStatement(x, y, left, right, top, bottom)
                
            elif self.current_token.value == 'FILL':
                self.eat(KEYWORD)
                pen = self.parse_expression()
                return FillStatement(pen)
                
            elif self.current_token.value == 'INK':
                self.eat(KEYWORD)
                pen = self.parse_expression()
                self.eat(SYMBOL) # ,
                color1 = self.parse_expression()
                color2 = None
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    color2 = self.parse_expression()
                return InkStatement(pen, color1, color2)

            elif self.current_token.value == 'PEN':
                self.eat(KEYWORD)
                stream = None
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                pen = None
                bg_mode = None
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    bg_mode = self.parse_expression()
                else:
                    pen = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                        bg_mode = self.parse_expression()
                return PenStatement(pen, bg_mode, stream)

            elif self.current_token.value == 'PAPER':
                self.eat(KEYWORD)
                stream = None
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                paper = self.parse_expression()
                return PaperStatement(paper, stream)
                
            elif self.current_token.value == 'GRAPHICS':
                self.eat(KEYWORD)
                if self.current_token.type == KEYWORD and self.current_token.value == 'PEN':
                    self.eat(KEYWORD)
                    pen = None
                    bg_mode = None
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                        bg_mode = self.parse_expression()
                    else:
                        pen = self.parse_expression()
                        if self.current_token.type == SYMBOL and self.current_token.value == ',':
                            self.eat(SYMBOL)
                            bg_mode = self.parse_expression()
                    return GraphicsPenStatement(pen, bg_mode)
                elif self.current_token.type == KEYWORD and self.current_token.value == 'PAPER':
                    self.eat(KEYWORD)
                    paper = self.parse_expression()
                    return GraphicsPaperStatement(paper)

            elif self.current_token.value == 'LOCATE':
                self.eat(KEYWORD)
                stream = None
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                col = self.parse_expression()
                self.eat(SYMBOL) # ,
                row = self.parse_expression()
                return LocateStatement(col, row, stream)

            elif self.current_token.value == 'CALL':
                self.eat(KEYWORD)
                address = self.parse_expression()
                params = []
                while self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    params.append(self.parse_expression())
                return CallStatement(address, params)

            elif self.current_token.value == 'PAUSE':
                self.eat(KEYWORD)
                time_expr = self.parse_expression()
                # We can reuse CallStatement with a dummy address for PAUSE or map it to CALL &BB18
                return CallStatement(Literal("&BB18", "HEX_NUMBER"), [])

            elif self.current_token.value == 'CLS':
                self.eat(KEYWORD)
                stream = None
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                return ClsStatement(stream)

            elif self.current_token.value == 'CLG':
                self.eat(KEYWORD)
                return ClgStatement()

            elif self.current_token.value == 'DI':
                self.eat(KEYWORD)
                return DiStatement()

            elif self.current_token.value == 'EI':
                self.eat(KEYWORD)
                return EiStatement()

            elif self.current_token.value == 'OPENIN':
                self.eat(KEYWORD)
                return OpenInStatement(self.parse_expression())

            elif self.current_token.value == 'OPENOUT':
                self.eat(KEYWORD)
                return OpenOutStatement(self.parse_expression())

            elif self.current_token.value == 'CLOSEIN':
                self.eat(KEYWORD)
                return CloseInStatement()

            elif self.current_token.value == 'CLOSEOUT':
                self.eat(KEYWORD)
                return CloseOutStatement()

            elif self.current_token.value in ('DEFINT', 'DEFREAL', 'DEFSTR'):
                type_name = self.current_token.value
                self.eat(KEYWORD)
                ranges = []
                while self.current_token.type == IDENTIFIER:
                    start_char = self.current_token.value
                    self.eat(IDENTIFIER)
                    if self.current_token.type == SYMBOL and self.current_token.value == '-':
                        self.eat(SYMBOL)
                        if self.current_token.type == IDENTIFIER:
                            end_char = self.current_token.value
                            self.eat(IDENTIFIER)
                            ranges.append((start_char[0].upper(), end_char[0].upper()))
                        else:
                            ranges.append((start_char[0].upper(), start_char[0].upper()))
                    else:
                        ranges.append((start_char[0].upper(), start_char[0].upper()))
                        
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                    else:
                        break
                return DefTypeStatement(type_name, ranges)

            elif self.current_token.value == 'BORDER':
                self.eat(KEYWORD)
                color1 = self.parse_expression()
                color2 = None
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    color2 = self.parse_expression()
                return BorderStatement(color1, color2)

            elif self.current_token.value == 'DEF':
                self.eat(KEYWORD)
                fn_name = ""
                if self.current_token.type == IDENTIFIER and self.current_token.value.upper() == 'FN':
                    self.eat(IDENTIFIER)
                    if self.current_token.type == IDENTIFIER:
                        fn_name = "FN" + self.current_token.value.upper()
                        self.eat(IDENTIFIER)
                    else:
                        fn_name = "FN"
                elif self.current_token.type == IDENTIFIER:
                    fn_name = self.current_token.value.upper()
                    self.eat(IDENTIFIER)
                        
                params = []
                if self.current_token.type == SYMBOL and self.current_token.value == '(':
                    self.eat(SYMBOL)
                    while self.current_token.type == IDENTIFIER:
                        params.append(self.current_token.value)
                        self.eat(IDENTIFIER)
                        if self.current_token.type == SYMBOL and self.current_token.value == ',':
                            self.eat(SYMBOL)
                        else:
                            break
                    if self.current_token.type == SYMBOL and self.current_token.value == ')':
                        self.eat(SYMBOL)
                        
                if self.current_token.type == SYMBOL and self.current_token.value == '=':
                    self.eat(SYMBOL)
                expr = self.parse_expression()
                return DefFnStatement(fn_name, params, expr)

            elif self.current_token.value == 'CLEAR':
                self.eat(KEYWORD)
                if self.current_token.type == KEYWORD and self.current_token.value == 'INPUT':
                    self.eat(KEYWORD)
                    return ClearInputStatement()
                return ClearStatement()

            elif self.current_token.value == 'RANDOMIZE':
                self.eat(KEYWORD)
                expr = None
                if self.current_token.type not in (NEWLINE, EOF, SYMBOL):
                    expr = self.parse_expression()
                return RandomizeStatement(expr)

            elif self.current_token.value == 'ERROR':
                self.eat(KEYWORD)
                code = self.parse_expression()
                return ErrorStatement(code)

            elif self.current_token.value == 'RESUME':
                self.eat(KEYWORD)
                is_next = False
                line_number = None
                if self.current_token.type == KEYWORD and self.current_token.value == 'NEXT':
                    self.eat(KEYWORD)
                    is_next = True
                elif self.current_token.type not in (NEWLINE, EOF) and not (self.current_token.type == SYMBOL and self.current_token.value == ':'):
                    line_number = self.parse_expression()
                return ResumeStatement(line_number, is_next)

            elif self.current_token.value == 'DEG':
                self.eat(KEYWORD)
                return DegStatement()

            elif self.current_token.value == 'RAD':
                self.eat(KEYWORD)
                return RadStatement()

            elif self.current_token.value == 'ENV':
                self.eat(KEYWORD)
                env_no = self.parse_expression()
                sections = []
                while self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    sections.append(self.parse_expression())
                return EnvStatement(env_no, sections)

            elif self.current_token.value == 'ENT':
                self.eat(KEYWORD)
                ent_no = self.parse_expression()
                sections = []
                while self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    sections.append(self.parse_expression())
                return EntStatement(ent_no, sections)

            elif self.current_token.value == 'SOUND':
                self.eat(KEYWORD)
                args = []
                args.append(self.parse_expression()) # channel
                for i in range(6): # remaining up to 6 args
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                        args.append(self.parse_expression())
                    else:
                        break
                
                # Fill missing args with None
                while len(args) < 7:
                    args.append(None)
                    
                return SoundStatement(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
        elif self.current_token.type == SYMBOL and self.current_token.value == '|':
            self.eat(SYMBOL)
            if self.current_token.type == IDENTIFIER:
                command = self.current_token.value.upper()
                self.eat(IDENTIFIER)
                params = []
                # Sometimes RSX commands have parameters starting with comma or directly
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                while self.current_token.type not in (NEWLINE, EOF) and not (self.current_token.type == SYMBOL and self.current_token.value == ':'):
                    if self.current_token.type == SYMBOL and self.current_token.value == '@':
                        self.eat(SYMBOL)
                        if self.current_token.type == IDENTIFIER:
                            params.append(Literal(self.current_token.value, STRING))
                            self.eat(IDENTIFIER)
                        else:
                            params.append(self.parse_expression())
                    else:
                        params.append(self.parse_expression())
                    
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                    else:
                        break
                return RsxStatement(command, params)
            else:
                # skip unknown statement
                while self.current_token.type not in (NEWLINE, EOF) and not (self.current_token.type == SYMBOL and self.current_token.value == ':'):
                    self.pos += 1
                    self.current_token = self.tokens[self.pos]
                return None

        elif self.current_token.type == IDENTIFIER:
            var_name = self.current_token.value
            self.eat(IDENTIFIER)
            if self.current_token.type == SYMBOL and self.current_token.value == '(':
                self.eat(SYMBOL)
                dims = []
                while True:
                    dims.append(self.parse_expression())
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                    else:
                        break
                self.eat(SYMBOL) # )
                if self.current_token.value == '=':
                    self.eat(SYMBOL)
                    expr = self.parse_expression()
                    return LetArrayStatement(var_name, dims, expr)
            elif self.current_token.value == '=':
                self.eat(SYMBOL)
                expr = self.parse_expression()
                return LetStatement(var_name, expr)
                
        return None

    def parse_expression(self):
        expr_tokens = []
        paren_level = 0
        expecting_op = False
        while self.current_token.type not in (NEWLINE, EOF):
            if self.current_token.type == SYMBOL and self.current_token.value == '(':
                paren_level += 1
            elif self.current_token.type == SYMBOL and self.current_token.value == ')':
                if paren_level == 0:
                    break
                paren_level -= 1
            
            if paren_level == 0 and self.current_token.type == SYMBOL and self.current_token.value in (',', ':', ';'):
                break
            if paren_level == 0 and self.current_token.type == KEYWORD and self.current_token.value in ('TO', 'STEP', 'THEN', 'GOTO', 'GOSUB', 'ELSE'):
                break
                
            # Break if we have two adjacent values (e.g. TAB(20) A$)
            is_value_start = self.current_token.type in ('IDENTIFIER', 'NUMBER', 'HEX_NUMBER', 'STRING') or \
                             (self.current_token.type == 'KEYWORD' and self.current_token.value not in ('MOD', 'AND', 'OR', 'XOR', 'NOT'))
            if paren_level == 0 and expecting_op and is_value_start:
                break
            
            # String literals are kept as Literal nodes directly to simplify
            if self.current_token.type == 'STRING' and not expr_tokens:
                val = self.current_token.value
                self.eat('STRING')
                return Literal(val, 'STRING')
                
            tok = self.current_token
            # FN merging
            if tok.type == 'IDENTIFIER' and tok.value.upper() == 'FN':
                next_tok = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
                if next_tok and next_tok.type == 'IDENTIFIER':
                    tok = Token('IDENTIFIER', "FN" + next_tok.value.upper(), tok.line, tok.column)
                    self.pos += 1
            
            expr_tokens.append(tok)
            
            if tok.type in ('IDENTIFIER', 'NUMBER', 'HEX_NUMBER', 'STRING') or (tok.type == 'SYMBOL' and tok.value == ')'):
                expecting_op = True
            elif tok.type == 'KEYWORD' and tok.value not in ('MOD', 'AND', 'OR', 'XOR', 'NOT'):
                expecting_op = True
            else:
                expecting_op = False
            
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
            
        if not expr_tokens:
            return None
            
        return RawExpression(expr_tokens)