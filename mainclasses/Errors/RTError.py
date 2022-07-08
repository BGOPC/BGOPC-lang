from .Error import Error
from ..utils.swa import swa

class RTError(Error):
    def __init__(self, pos_start, pos_end, name=None,message=None, context=None):
        self.context = context
        if message and name:
            super().__init__(pos_start, pos_end, f"Runtime Error: {name}", message)
        elif message:
            super().__init__(pos_start, pos_end, f"Runtime Error", message)
        else:
            self.pos_start = pos_start
            self.pos_end = pos_end
    def as_string(self):
        result = self.generate_tb()
        result += f'{self.error_name}: {self.details}\n'
        result += '\n' + swa(self.pos_start.ftxt, self.pos_start, self.pos_end)

        return result
    def generate_tb(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        return "Trace Back Result\n" + result

    def divbyzero(self, msg):
        return DivByZero(self.pos_start, self.pos_end, msg, self.context)

class DivByZero(RTError):
    def __init__(self, pos_start, pos_end, message,context=None):
        super().__init__(pos_start, pos_end, "Division By Zero", message, context)
