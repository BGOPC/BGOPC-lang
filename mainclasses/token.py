import string
DIGITS = "0123456789"
LETTERS = string.ascii_letters
DIGITS_LETTERS = DIGITS+LETTERS
KEYWORDS = [
    "Var", "var",
    "And", "and",
    "Or", "or",
    "Not", "not",
    "If", "if","then","}",
    "else", "Else",
    "ElseIf", "elseif",
    "to","To",
    "stp",
    "For","for",
    "while", "While",
]

class enums:
    INT = "Integer"
    FLOAT = "Float"
    PLUS = "Plus"
    MIN = "Minus"
    DIV = "Divide"
    MUL = "Multiply"
    LPAREN = "Left Parenthesis"
    RPAREN = "Right Parenthesis"
    EOF = "End of File"
    POW = "Power"
    IDENTIFIER = "Identifier"
    KEYWORD = "Keyword"
    EQ = "EQ"
    NE = "Not Equals"
    EE = "EE"
    LT = "LT"
    LTE = "LTE"
    GT = "GT"
    GTE = "GTE"


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    def matches(self,type, val):
        return self.type == type and self.value == val