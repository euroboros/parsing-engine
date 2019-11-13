"A file with some objects used on the program."

# class Token:

#     """The base element for parsing."""

#     def __init__(self, type_, value=None):
#         self.type = type_
#         self.value = value

#     def __repr__(self):
#         return_ = f'Token({self.type}'
#         if self.value != None:
#             return_ += f', {self.value.__repr__()}'
#         return_ += ')'
#         return return_

#     __str__ = __repr__

class ParsingElement:

    """A base for elements used on parsing and lexing."""

    def __init__(self, head, *body):
        self.head = head
        self.body = body

    def __repr__(self):

        # Create the output variable and add some values to it, one by one.
        rep = self.__class__.__name__ # Class name
        rep += f'({self.head.__repr__()})'
        if len(self.body) != 0:
            rep += f': {", ".join([str(x).__repr__() for x in self.body])}'

        # Return results
        return rep

    __str__ = __repr__

class Action(ParsingElement):
    """An element used by the lexer to understand tokens without too much complexity."""

class Token(ParsingElement):
    """An element generated by the lexer and understood by the parses that represents the bits of codes, the symbols on the code string."""

class ActionStack:

    """The class stack used on the lexer."""

    def __init__(self):
        pass
