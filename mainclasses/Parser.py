from .utils.Nodes.BinOpNode import BinOpNode
from .utils.Nodes.NumberNode import NumberNode
from .utils.Nodes.UnaryOpNode import UnaryOpNode
from .utils.Nodes.IfNodes import *
from .utils.Nodes.VarNodes import *
from .utils.Nodes.LoopsNodes import *
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
            self.cc: Token = self.tokens[self.tok_idx]
        return self.cc

    def atom(self):
        res = ParseResult()
        tok = self.cc

        if tok.type in (enums.INT, enums.FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type in enums.IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == enums.LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.cc.type == enums.RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.cc.pos_start, self.cc.pos_end,
                    "Expected ')'"
                ))
        elif  tok.matches(enums.KEYWORD, "If") or tok.matches(enums.KEYWORD, "if"):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)
        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int, float, identifier,'+', '-' or '('"
        ))
    def power(self):
        return self.binop(self.atom, (enums.POW, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.cc

        if tok.type in (enums.PLUS, enums.MIN):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        return self.power()


    def expr(self):
        res = ParseResult()

        if self.cc.matches(enums.KEYWORD, 'Var') or self.cc.matches(enums.KEYWORD, 'var'):
            res.register_advancement()
            self.advance()

            if self.cc.type != enums.IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.cc.pos_start, self.cc.pos_end,
                    "Expected identifier"
                ))

            var_name = self.cc
            res.register_advancement()
            self.advance()

            if self.cc.type != enums.EQ:
                return res.failure(InvalidSyntaxError(
                    self.cc.pos_start, self.cc.pos_end,
                    "Expected '='"
                ))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.binop(self.comp_expr,((enums.KEYWORD , "and"), (enums.KEYWORD , "or"),(enums.KEYWORD , "And"), (enums.KEYWORD , "Or"))))
        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.cc.pos_start, self.cc.pos_end,
                    "Excepted Variable,(Var Assignment), int, float, identifier, '+', '-' or '('"
                )
            )

        return res.success(node)
    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not (self.cc.matches(enums.KEYWORD, 'If') or self.cc.matches(enums.KEYWORD, "if")):
            return res.failure(InvalidSyntaxError(
                self.cc.pos_start, self.cc.pos_end,
                f"Expected 'IF'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.cc.matches(enums.KEYWORD, 'then'):
            return res.failure(InvalidSyntaxError(
                self.cc.pos_start, self.cc.pos_end,
                "Expected 'then' ",
            ))

        res.register_advancement()
        self.advance()

        expr = res.register(self.expr())
        if res.error: return res
        cases.append((condition, expr))

        while self.cc.matches(enums.KEYWORD, 'elseif') or self.cc.matches(enums.KEYWORD, "ElseIf"):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expr())
            if res.error: return res

            if not self.cc.matches(enums.KEYWORD, 'then'):
                return res.failure(InvalidSyntaxError(
                    self.cc.pos_start, self.cc.pos_end,
                    "Expected 'then'"
                ))

            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())
            if res.error: return res
            cases.append((condition, expr))

        if self.cc.matches(enums.KEYWORD, 'else') or self.cc.matches(enums.KEYWORD, "Else"):
            res.register_advancement()
            self.advance()
            if not self.cc.matches(enums.KEYWORD, 'then'):
                return res.failure(InvalidSyntaxError(
                    self.cc.pos_start, self.cc.pos_end,
                    "Expected 'then'"
                ))
            res.register_advancement()
            self.advance()
            else_case = res.register(self.expr())
            
            if res.error: return res

        return res.success(IfNode(cases, else_case))

    def term(self):
        return self.binop(self.factor, (enums.MUL,enums.DIV))
    def for_expr(self):
        res = ParseResult()

        if not( self.current_tok.matches(enums.KEYWORD, 'for') or  self.current_tok.matches(enums.KEYWORD, 'For')):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'FOR'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != enums.IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected identifier"
            ))

        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != enums.EQ:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '='"
            ))
        
        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error: return res

        if not (self.current_tok.matches(enums.KEYWORD, 'to') or  self.current_tok.matches(enums.KEYWORD, 'To')):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'TO'"
            ))
        
        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error: return res

        if self.current_tok.matches(enums.KEYWORD, 'stp'):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error: return res
        else:
            step_value = None

        if not self.current_tok.matches(enums.KEYWORD, 'then'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'then'"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error: return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body))

    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(enums.KEYWORD, 'WHILE'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'WHILE'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(enums.KEYWORD, 'then'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'then'"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error: return res

        return res.success(WhileNode(condition, body))

    def binop(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.cc.type in ops or (self.cc.type, self.cc.value) in ops:
            op_tok = self.cc
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)
    def comp_expr(self):
        res = ParseResult()
        if self.cc.matches(enums.KEYWORD, "Not") or self.cc.matches(enums.KEYWORD, "not"):
            op_tok = self.cc
            res.register_advancement()
            self.advance()
            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok=op_tok, node=node))
        node = res.register(self.binop(self.arith_expr, (enums.EE, enums.NE, enums.LT, enums.LTE, enums.GT, enums.GTE)))
        if res.error:
            return res.failure(
             InvalidSyntaxError(
            self.cc.pos_start, self.cc.pos_end,
            "Expected int, float, identifier,'+', '-', '(' or 'not'"
            )
        )
        return res.success(node)


    def arith_expr(self):
        return self.binop(self.term, (enums.PLUS, enums.MIN))
    def parse(self):
        res = self.expr()
        if not res.error and self.cc.type != enums.EOF:
            return res.failure(
                InvalidSyntaxError(
                    self.cc.pos_start, self.cc.pos_end,
                    "Excepted '+', '-', '*', '/' or '^' "
                )
            )
        return res


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0
    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self
    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self
