from ..Errors.RTError import RTError
class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self,context=None):
        self.context = context
        return self

    def add(self, number):
        if isinstance(number, Number):
            return Number(self.value + number.value).set_context(self.context), None
    def sub(self, number):
        if isinstance(number, Number):
            return Number(self.value - number.value).set_context(self.context), None
    def mul(self, number):
        if isinstance(number, Number):
            return Number(self.value * number.value).set_context(self.context), None
    def div(self, number):
        if isinstance(number, Number):
            if number.value == 0:
                return None,RTError(pos_start=number.pos_start, pos_end=number.pos_end,context=self.context).divbyzero(
                        f"You Can not Divide {self.value} by 0",

                    )
            return Number(self.value / number.value).set_context(self.context), None

    def __repr__(self):
        return str(self.value)