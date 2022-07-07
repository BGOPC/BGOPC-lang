from .utils.Nodes.BinOpNode import BinOpNode
from .utils.Nodes.NumberNode import NumberNode
from .utils.Nodes.UnaryOpNode import UnaryOpNode
from .token import enums, Token
from .Errors.InvalidSyntaxError import InvalidSyntaxError
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
        res = ParseResult()
        tok = self.cc

        if tok.type in (enums.PLUS, enums.MIN):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.type in (enums.INT, enums.FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == enums.LPAREN:
                res.register(self.advance())
                expr = res.register(self.expr())
                if res.error: return res
                if self.cc.type == enums.RPAREN:
                    res.register(self.advance())
                    return res.success(expr)
                else:
                    return res.failure(InvalidSyntaxError(
                        self.cc.pos_start, self.cc.pos_end,
                        "Expected ')'"
                    ))

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int or float"
            ))


    def expr(self):
        return self.binop((enums.PLUS,enums.MIN), self.term)


    def term(self):
        return self.binop((enums.MUL,enums.DIV), self.factor)

    def binop(self, toks, func):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.cc.type in toks:
            op_tok = self.cc
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)
        return res.success(left)

    def parse(self):
        res = self.expr()
        if not res.error and self.cc.type != enums.EOF:
            return res.failure(
                InvalidSyntaxError(
                    self.cc.pos_start, self.cc.pos_end,
                    "Excepted '+', '-', '*' or '/'"
                )
            )
        return res


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res ):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self
    def failure(self, error):
        self.error = error
        return self