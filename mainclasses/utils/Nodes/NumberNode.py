from mainclasses.token import Token # , enums
class NumberNode:
    def __init__(self, tok: Token):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    def __repr__(self) -> str:
        return f"{self.tok}"
