DIGITS = "0123456789"
class enums:
    INT = "Integer"
    FLOAT = "Float"
    PLUS = "Plus"
    MIN = "Minus"
    DIV = "Divide"
    MUL = "Multiply"
    LPAREN = "Left Parenthesis"
    RPAREN = "Right Parenthesis"


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
    def __repr__(self):
        if self.value: return f"{self.type}:{self.value}"
        return str(self.type)
