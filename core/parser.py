from core.lexer import Lexer, EOF, NUMBER, HEX_NUMBER, STRING, IDENTIFIER, KEYWORD, SYMBOL, NEWLINE

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

class InputStatement(Statement):
    def __init__(self, prompt, variables):
        self.prompt = prompt
        self.variables = variables

class SymbolStatement(Statement):
    def __init__(self, char_code, matrix):
        self.char_code = char_code
        self.matrix = matrix

class FrameStatement(Statement):
    pass

class StopStatement(Statement):
    pass

class WindowStatement(Statement):
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

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
    def __init__(self, x, y, pen=None):
        self.x = x
        self.y = y
        self.pen = pen

class DrawrStatement(Statement):
    def __init__(self, x, y, pen=None):
        self.x = x
        self.y = y
        self.pen = pen

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
    def __init__(self, pen):
        self.pen = pen
        
class PaperStatement(Statement):
    def __init__(self, paper):
        self.paper = paper

class LocateStatement(Statement):
    def __init__(self, col, row):
        self.col = col
        self.row = row

class ClsStatement(Statement):
    pass

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
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression() # stream
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                exprs = []
                while self.current_token.type not in (NEWLINE, EOF) and not (self.current_token.type == SYMBOL and self.current_token.value == ':'):
                    if self.current_token.type == SYMBOL and self.current_token.value in (';', ','):
                        exprs.append(Literal(self.current_token.value, "SEPARATOR"))
                        self.eat(SYMBOL)
                    else:
                        expr = self.parse_expression()
                        if expr is not None:
                            exprs.append(expr)
                        else:
                            break
                return PrintStatement(exprs)
            
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
                    expr = self.parse_expression()
                    if expr is not None:
                        values.append(expr)
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
                        variables.append(self.current_token.value)
                        self.eat(IDENTIFIER)
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

            elif self.current_token.value == 'INPUT':
                self.eat(KEYWORD)
                prompt = None
                # Check if there is a prompt string
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
                return InputStatement(prompt, variables)

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
                # optionally #channel,
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression() # channel
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL) # ,
                left = self.parse_expression()
                self.eat(SYMBOL)
                right = self.parse_expression()
                self.eat(SYMBOL)
                top = self.parse_expression()
                self.eat(SYMBOL)
                bottom = self.parse_expression()
                return WindowStatement(left, right, top, bottom)

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
                        stmt = self.parse_statement()
                        if stmt:
                            then_stmts.append(stmt)
                        if self.current_token.type == SYMBOL and self.current_token.value == ':':
                            self.eat(SYMBOL)
                            
                # Parse ELSE branch
                if self.current_token.type == KEYWORD and self.current_token.value == 'ELSE':
                    self.eat(KEYWORD)
                    if self.current_token.type == NUMBER:
                        line_num = self.parse_expression()
                        else_stmts.append(GotoStatement(line_num))
                    else:
                        while self.current_token.type not in (NEWLINE, EOF):
                            stmt = self.parse_statement()
                            if stmt:
                                else_stmts.append(stmt)
                            if self.current_token.type == SYMBOL and self.current_token.value == ':':
                                self.eat(SYMBOL)
                
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
                mask = self.parse_expression()
                first_point = None
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
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    pen = self.parse_expression()
                return DrawStatement(x, y, pen)

            elif self.current_token.value == 'DRAWR':
                self.eat(KEYWORD)
                x = self.parse_expression()
                self.eat(SYMBOL) # ,
                y = self.parse_expression()
                pen = None
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    pen = self.parse_expression()
                return DrawrStatement(x, y, pen)

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
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression() # stream
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                pen = self.parse_expression()
                return PenStatement(pen)

            elif self.current_token.value == 'PAPER':
                self.eat(KEYWORD)
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression() # stream
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                paper = self.parse_expression()
                return PaperStatement(paper)

            elif self.current_token.value == 'LOCATE':
                self.eat(KEYWORD)
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression() # stream
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                col = self.parse_expression()
                self.eat(SYMBOL) # ,
                row = self.parse_expression()
                return LocateStatement(col, row)

            elif self.current_token.value == 'CLS':
                self.eat(KEYWORD)
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression() # stream
                return ClsStatement()

            elif self.current_token.value == 'CLG':
                self.eat(KEYWORD)
                return ClgStatement()

            elif self.current_token.value == 'BORDER':
                self.eat(KEYWORD)
                color1 = self.parse_expression()
                color2 = None
                if self.current_token.type == SYMBOL and self.current_token.value == ',':
                    self.eat(SYMBOL)
                    color2 = self.parse_expression()
                return BorderStatement(color1, color2)

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
            
            # String literals are kept as Literal nodes directly to simplify
            if self.current_token.type == STRING and not expr_tokens:
                val = self.current_token.value
                self.eat(STRING)
                return Literal(val, STRING)
                
            expr_tokens.append(self.current_token)
            
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
            
        if not expr_tokens:
            return None
            
        return RawExpression(expr_tokens)