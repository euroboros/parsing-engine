"A file with some objects used on the program."

class Token:

    """The base element for parsing."""

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return_ = f'Token({self.type}'
        if self.value != None:
            return_ += f', {self.value.__repr__()}'
        return_ += ')'
        return return_

    __str__ = __repr__

class Action:

    """An element used by the lexer to understand tokens without too much complexity."""

    def __init__(self, head, *body):
        self.head = head
        self.body = body

    def __repr__(self):
        return_ = f'Action({self.head}'
        if len(self.body) != 0:
            return_ += ', ({}'.format(', '.join(self.body))
        return_ += ')'
        return return_

    __str__ = __repr__
