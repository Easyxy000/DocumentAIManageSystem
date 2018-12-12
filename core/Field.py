class Field:
    def __init__(self, id, name, defaultSize=100,formatMethod=None,hasValue=True, editable=False, reverse=False, comparable=True, delegateClass=None, delegateParameters=None):
        self.id = id
        self.name = name
        self.formatMethod = formatMethod
        self.hasValue = hasValue
        self.editable = editable
        self.reverse = reverse
        self.comparable = comparable
        self.delegateClass = delegateClass
        self.delegateParameters = [] if delegateParameters is None else delegateParameters
        self.defaultSize = defaultSize