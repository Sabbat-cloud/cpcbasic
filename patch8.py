import sys

with open('core/parser.py', 'r') as f:
    code = f.read()

code = code.replace('''            elif self.current_token.value == 'LOCATE':
                self.eat(KEYWORD)
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression() # stream
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                col = self.parse_expression()''', '''            elif self.current_token.value == 'LOCATE':
                self.eat(KEYWORD)
                stream = None
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                col = self.parse_expression()''')

code = code.replace('''            elif self.current_token.value == 'WINDOW':
                self.eat(KEYWORD)
                # optionally #channel,
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression() # channel
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL) # ,
                left = self.parse_expression()''', '''            elif self.current_token.value == 'WINDOW':
                self.eat(KEYWORD)
                stream = None
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                left = self.parse_expression()''')

code = code.replace('''            elif self.current_token.value == 'PEN':
                self.eat(KEYWORD)
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    self.parse_expression() # stream
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                pen = None''', '''            elif self.current_token.value == 'PEN':
                self.eat(KEYWORD)
                stream = None
                if self.current_token.type == SYMBOL and self.current_token.value == '#':
                    self.eat(SYMBOL)
                    stream = self.parse_expression()
                    if self.current_token.type == SYMBOL and self.current_token.value == ',':
                        self.eat(SYMBOL)
                pen = None''')

with open('core/parser.py', 'w') as f:
    f.write(code)

