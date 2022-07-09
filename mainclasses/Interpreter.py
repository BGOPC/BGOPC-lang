from mainclasses.utils.Nodes.VarNodes import VarAccessNode, VarAssignNode
from .utils.Nodes.NumberNode import NumberNode
from .utils.Nodes.BinOpNode import BinOpNode
from .utils.Nodes.UnaryOpNode import UnaryOpNode
from .utils.Nodes.IfNodes import *
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

    def visit_VarAccessNode(self, node: VarAccessNode, context:Context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(node.pos_start,node.pos_end, context=context).varnotdef(
                f"Variable {var_name} is not defined",
            ))
        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)



    def visit_VarAssignNode(self, node: VarAssignNode, context: Context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res
        context.symbol_table.set(var_name, value)
        return res.success(value)


    def visit_NumberNode(self, node, context:Context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left: Number = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res
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
        elif node.op_tok.type == enums.EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == enums.NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == enums.LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == enums.GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == enums.LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == enums.GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(enums.KEYWORD, 'and') or node.op_tok.matches(enums.KEYWORD, 'And'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(enums.KEYWORD, 'Or') or node.op_tok.matches(enums.KEYWORD, 'or'):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)

        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number:Number = res.register(self.visit(node.node, context))
        if res.error: return res
        error = None
        if node.op_tok.type == enums.MIN:
            number, error = number.mul(Number(-1))
        elif node.op_tok.matches(enums.KEYWORD, 'Not') or node.op_tok.matches(enums.KEYWORD, 'not'):
            number, error = number.notted()
        if error:
            return res.failure(error)
        return res.success(number.set_pos(node.pos_start, node.pos_end))
    
    def visit_IfNode(self, node:IfNode, context):
        res = RTResult()
        for condition,expr in node.cases:
            cond_val:Number = res.register(self.visit(condition, context))
            if res.error: return res

            if cond_val.is_true():
                expr_val = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_val)
        if node.else_case:
            else_val = res.register(self.visit(node.else_case, context))
            if res.error: return res
            return res.success(else_val)
        return res.success(None)