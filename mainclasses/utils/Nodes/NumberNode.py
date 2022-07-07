from mainclasses.token import Token # , enums
class NumberNode:
    def __init__(self, tok: Token):
        self.tok = tok

    def __repr__(self) -> str:
        return f"{self.tok}"
