from .utils.Nodes.NumberNode import NumberNode
from .utils.Nodes.BinOpNode import BinOpNode
from .utils.Nodes.UnaryOpNode import UnaryOpNode
from .utils.DataTypes import *
from .token import enums, Token

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit method for {type(node).__name__} is defined')

    def visit_NumberNode(self, node):
        return Number(node.tok.value).set_pos(node.pos_start, node.pos_end)
    def visit_BinOpNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        if node.op_tok.type == enums.PLUS:
            result = left.add(right)
        elif node.op_tok.type == enums.MIN:
            result = left.sub(right)
        elif node.op_tok.type == enums.DIV:
            result = left.div(right)
        elif node.op_tok.type == enums.MUL:
            result = left.mul(right)

        return result.set_pos(node.pos_start, node.pos_end)

    def visit_UnaryOpNode(self, node):
        number = self.visit(node.node)
        if node.op_tok.type == enums.MIN:
            number = number.mul(Number(-1))
        return number.set_pos(node.pos_start, node.pos_end)