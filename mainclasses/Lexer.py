from .Errors.Error import Error
from .Errors.IllegalCharError import IllegalCharError
from .Errors.ExpectedCharError import ExpectedCharError
from .token import *
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
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '=':
                tokens.append(self.make_eq())
                self.advance()
            elif self.current_char == '<':
                tokens.append(self.make_lt())
                self.advance()
            elif self.current_char == '>':
                tokens.append(self.make_gt())
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(enums.PLUS, pos_start = self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(enums.MIN, pos_start = self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(self.make_pom())
            elif self.current_char == '/':
                tokens.append(Token(enums.DIV, pos_start = self.pos))
                self.advance()
            elif self.current_char == '!':
                tok, error = self.make_neq() # not equal
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '(':
                tokens.append(Token(enums.LPAREN, pos_start = self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(enums.RPAREN, pos_start = self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
        tokens.append(Token(enums.EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(enums.INT, int(num_str),pos_start=pos_start, pos_end=self.pos)
        else:
            return Token(enums.FLOAT, float(num_str),pos_start=pos_start, pos_end=self.pos)

    def make_pom(self): #Pow or Mul
        self.advance()
        ncc = self.current_char
        if ncc == "*":
            self.advance()
            return Token(enums.POW, pos_start=self.pos)
        return Token(enums.MUL, pos_start=self.pos)
    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS_LETTERS + '_':
            id_str += self.current_char
            self.advance()

        tok_type = enums.KEYWORD if id_str in KEYWORDS else enums.IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)
    def make_neq(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(enums.NE, pos_start=pos_start, pos_end=self.pos), None
        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' after '!'")

    def make_eq(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            return Token(enums.EE, pos_start=pos_start, pos_end=self.pos)
        return Token(enums.EQ, pos_start=pos_start, pos_end=self.pos)

    def make_gt(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            return Token(enums.GTE, pos_start=pos_start, pos_end=self.pos)
        return Token(enums.GT, pos_start=pos_start, pos_end=self.pos)

    def make_lt(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            return Token(enums.LTE, pos_start=pos_start, pos_end=self.pos)
        return Token(enums.LT, pos_start=pos_start, pos_end=self.pos)