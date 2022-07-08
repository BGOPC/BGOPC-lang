from .Error import Error

class RTError(Error):
    def __init__(self, pos_start, pos_end, name=None,message=None):
        if message and name:
            super().__init__(pos_start, pos_end, f"Runtime Error: {name}", message)
        elif message:
            super().__init__(pos_start, pos_end, f"Runtime Error", message)
        else:
            self.pos_start = pos_start
            self.pos_end = pos_end
    def divbyzero(self, msg):
        return DivByZero(self.pos_start, self.pos_end, msg)

class DivByZero(RTError):
    def __init__(self, pos_start, pos_end, message):
        super().__init__(pos_start, pos_end, "Division By Zero", message)