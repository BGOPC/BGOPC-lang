from .utils.Nodes.BinOpNode import BinOpNode
from .utils.Nodes.NumberNode import NumberNode

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx > len(self.tokens):
            return None
        return  self.tokens[self.tok_idx]