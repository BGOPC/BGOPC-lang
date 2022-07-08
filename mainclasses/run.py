from .Lexer import Lexer
from .Parser import Parser
from .Interpreter import Interpreter
from .utils.Context import Context
from .utils.SymbolTable import SymbolTable
from .utils.DataTypes import *
global_symboltable = SymbolTable()
global_symboltable.set("null", Number(0))
global_symboltable.set("nil", Number(0))
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symboltable
    res = interpreter.visit(ast.node, context)
    return res.value, res.error
