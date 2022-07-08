class Context:
    def __init__(self, name, parent=None, parent_entry=None):
        self.name = name
        self.parent = parent
        self.parent_entry_pos = parent_entry
        