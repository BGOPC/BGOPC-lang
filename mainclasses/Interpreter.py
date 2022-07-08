from .utils.Nodes.NumberNode import NumberNode
from .utils.Nodes.BinOpNode import BinOpNode
from .utils.Nodes.UnaryOpNode import UnaryOpNode
from .utils.DataTypes import *
from .token import enums, Token
from .RTResult import RTResult
class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit method for {type(node).__name__} is defined')

    def visit_NumberNode(self, node):
        return RTResult().success(
            Number(node.tok.value).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinOpNode(self, node):
        res = RTResult()
        left = res.register(self.visit(node.left_node))
        if res.error: return res
        right = res.register(self.visit(node.right_node))

        if node.op_tok.type == enums.PLUS:
            result, error = left.add(right)
        elif node.op_tok.type == enums.MIN:
            result, error = left.sub(right)
        elif node.op_tok.type == enums.DIV:
            result, error = left.div(right)
        elif node.op_tok.type == enums.MUL:
            result, error = left.mul(right)

        if error:
            return res.failure(error)

        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node):
        res = RTResult()
        number = res.register(self.visit(node.node))
        if res.error: return res
        error = None
        if node.op_tok.type == enums.MIN:
            number, error = number.mul(Number(-1))
        if error:
            return res.failure(error)
        return res.success(number.set_pos(node.pos_start, node.pos_end))