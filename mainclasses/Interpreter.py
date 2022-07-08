from .utils.Nodes.NumberNode import NumberNode
from .utils.Nodes.BinOpNode import BinOpNode
from .utils.Nodes.UnaryOpNode import UnaryOpNode
from .utils.DataTypes import *
from .token import enums, Token
from .RTResult import RTResult
from .utils.Context import Context
class Interpreter:
    def visit(self, node, context:Context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context:Context):
        raise Exception(f'No visit method for {type(node).__name__} is defined')

    def visit_NumberNode(self, node, context:Context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))

        if node.op_tok.type == enums.PLUS:
            result, error = left.add(right)
        elif node.op_tok.type == enums.MIN:
            result, error = left.sub(right)
        elif node.op_tok.type == enums.DIV:
            result, error = left.div(right)
        elif node.op_tok.type == enums.MUL:
            result, error = left.mul(right)
        elif node.op_tok.type == enums.POW:
            result, error = left.pow(right)

        if error:
            return res.failure(error)

        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res
        error = None
        if node.op_tok.type == enums.MIN:
            number, error = number.mul(Number(-1))
        if error:
            return res.failure(error)
        return res.success(number.set_pos(node.pos_start, node.pos_end))