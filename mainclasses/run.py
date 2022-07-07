from .Lexer import Lexer
from .Parser import Parser
from .Interpreter import Interpreter

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    interpreter = Interpreter()
    res = interpreter.visit(ast.node)
    return res, None
