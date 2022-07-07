from .utils.Nodes.BinOpNode import BinOpNode
from .utils.Nodes.NumberNode import NumberNode
from .token import enums, Token
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.cc = self.tokens[self.tok_idx]
        return self.cc

    def factor(self):
        tok = self.cc
        if tok.type in (enums.INT, enums.FLOAT):
            self.advance()
            return NumberNode(tok)
    def expr(self):
        return self.binop((enums.PLUS,enums.MIN), self.term)
    def term(self):
        return self.binop((enums.MUL,enums.DIV), self.factor)


    def binop(self, toks, func):
        left = func()
        while self.cc.type in toks:
            op_tok = self.cc
            self.advance()
            right = func()
            left = BinOpNode(left, op_tok, right)
        return left

    def parse(self):
        res = self.expr()
        return res