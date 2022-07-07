from .Error import Error

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, message):
        super().__init__(pos_start, pos_end, "Invalid Syntax", message)