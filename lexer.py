"""The component of the program that analyzes the original strings and parses them, returning tokens."""

# Initial imports
from objects import Token, Action, ActionStack

# Make some exception types.
class LexicalError(Exception): ...

def generate_context_stack():

    """Generates the context stack.

    The context stack is used by the lexer to understand what type of data is being read at a specific point on the "string to be analyzed".

    The lexer should always use the last element of the list - that is, the -1st element.

    Values' meanings:
    'top' := Is the first item on the stack, which means "the main level". It's here that functions and variables are understood.
    'literal_string_1' := Means that the lexer is currently analyzing string data that started with the 'one quote symbol'.
    'literal_string_2' := Means that the lexer is currently analyzing string data that started with the "double quote symbol".
    'literal_number' := Means that the lexer is currently analyzing a number, be it an integer or a float.
    'string_escape' := Means that the lexer is currently analyzing an escape character inside a string.
    'top_escape' := Means that the lexer is currently analyzing an escape character outside a string (e.g. the \\ commonly used on the end of a line to make it possible to continue the same command on another line).
    'paren' := Means that the lexer is analyzing data inside parentheses.

    I could just have added the list below directly to the parser function, but I thought making a function for this would make it easier to understand.
    """

    return ['top']

def lexical_analysis(code_string):

    """Parses the code provided on the argument and returns a list of tokens."""

    if len(code_string) != 0:
        if code_string[-1] != '\n':
            code_string += '\n'

    tokens = []
    queue = ''
    context_stack = generate_context_stack()
    # action_stack = ActionStack() # Still need to develop.

    # Valid chars for indentifiers.
    VALID_IDENTIFIER_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_:'

    for (char_index, char) in enumerate(code_string):

        # Create an action stack
        # Action stacks are used to apply actions on the queue, tokens list and context stack without needing to repeat the same actions multiple times on the situations below.
        # Each action is a tuple, with the first item being the action head (the "thing to do") and the other items (the amount depends on how many arguments the head needs) are the action body.
        action_stack = []

        # Checks on the "top" context
        if context_stack[-1] == 'top':

            if queue == '':

                # Start a string
                if char == '\'':
                    action_stack.append(Action('enter_context', 'literal_string_1'))
                elif char == '\"':
                    action_stack.append(Action('enter_context', 'literal_string_2'))

                # Start a number literal
                elif char in '0123456789':
                    action_stack.append(Action('enter_context', 'literal_number'))
                    action_stack.append(Action('queue_append', char))

                # Start an indentifier token
                elif char in VALID_IDENTIFIER_CHARS:
                    action_stack.append(Action('enter_context', 'identifier'))
                    action_stack.append(Action('queue_append', char))

                # End of line
                elif char in {'\n', ';'}:
                    action_stack.append(Action('eol'))

            else:

                # Invalid characters
                # Here lies characters that might mean something, but are on the wrong context.
                if char in {'\'', '\"'}:
                    raise LexicalError(f'char {char.__repr__()} out of context')

                # EOL characters
                # They separate commands. That's it.
                if char in {'\n', ';'}:
                    action_stack.append(Action('eol'))

        # The checks below happen also when the new context is added to the stack (since I'm not using elif on the first one)

        if context_stack[-1].startswith('literal_string_'):

            if ((char == '\'' and context_stack[-1][-1] == '1') or
               (char == '\"' and context_stack[-1][-1] == '2')):
                # End the string
                action_stack.append(Action('end_context'))

            # Or else, append the current character to the string.
            # NOTE: I'm not sure if it is a good idea to use the action stack to append something to the queue, but for now I'll keep it.
            else:
                action_stack.append(Action('queue_append', char))

            # TODO: Handle Escape Characters

        elif context_stack[-1] == 'literal_number':

            if char in '0123456789':
                action_stack.append(Action('queue_append', char))

            # EOL Characters
            elif char in {'\n', ';'}:
                action_stack.append(Action('end_context'))
                action_stack.append(Action('eol'))

            else:
                raise LexicalError(f'char {char.__repr__()} not understood while parsing a literal_number')

        elif context_stack[-1] == 'identifier':

            if char in VALID_IDENTIFIER_CHARS:
                action_stack.append(Action('queue_append', char))
            else:
                action_stack.append(Action('end_context', char))
                if char in {'\n', ';'}:
                    action_stack.append(Action('eol'))
                # There should be more of these. Because of that, I might need to make more functions.

        # Process the action stack.
        for action in action_stack:

            if action.head == 'enter_context':
                context_stack.append(action.body[0])

            elif action.head == 'eol':
                tokens.append(Token('eol'))

            elif action.head == 'queue_append':
                queue += action.body[0]

            elif action.head == 'end_context':

                token_head = None
                token_body = None

                if context_stack[-1].startswith('literal_string_'):
                    token_head = 'str'
                    token_body = queue

                elif context_stack[-1] == 'literal_number':
                    # TODO: add here part of the support for more number types (like float)
                    token_head = 'int'
                    token_body = int(queue)

                elif context_stack[-1] == 'identifier':
                    token_head = 'identifier'
                    token_body = queue

                # token_to_append = Token(token_head, queue)
                token_to_append = Token(token_head, token_body)
                tokens.append(token_to_append)

                # Clear the queue and remove the current context from the stack
                queue = ''
                del context_stack[-1]

            else:
                raise LexicalError(f'Invalid action: {action}')

    return tokens
