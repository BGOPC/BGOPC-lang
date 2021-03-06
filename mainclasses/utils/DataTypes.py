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
    def pow(self, number):
        if isinstance(number, Number):
            return Number(self.value ** number.value).set_context(self.context), None
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0
    def __repr__(self):
        return str(self.value)