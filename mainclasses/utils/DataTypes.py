class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def add(self, number):
        if isinstance(number, Number):
            return Number(self.value + number.value)
    def sub(self, number):
        if isinstance(number, Number):
            return Number(self.value - number.value)
    def mul(self, number):
        if isinstance(number, Number):
            return Number(self.value * number.value)
    def div(self, number):
        if isinstance(number, Number):
            return Number(self.value / number.value)

    def __repr__(self):
        return str(self.value)