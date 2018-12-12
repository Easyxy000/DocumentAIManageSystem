class Field:
    def __init__(self, id, name, formatMethod=None, editable=False, reverse=False, comparable=True, delegateClass=None):
        self.id = id
        self.name = name
        self.formatMethod = formatMethod
        self.editable = editable
        self.reverse = reverse
        self.comparable = comparable
        self.delegateClass = delegateClass