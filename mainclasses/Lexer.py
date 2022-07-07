from .token import *
from .Errors.Error import Error
from .Errors.IllegalCharError import IllegalCharError
from .utils.position import Position
class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(enums.PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(enums.MIN))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(enums.MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(enums.DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(enums.LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(enums.RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(enums.INT, int(num_str))
        else:
            return Token(enums.FLOAT, float(num_str))