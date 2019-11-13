#!/usr/bin/env python3

def generate_syntax_tree(list_, level=0):

    """Turns the lexical analysis output into a tree."""

    for token in list_:

        print('  '*level + '- Token: ' + token.head)
        if token.body: # Check if the token body is not empty.
            print('  '*(level+1) + 'Type: ' + str(token.body))

def complete_analysis(string):

    import lexer
    import pprint

    print(f'\033[34mRaw String:\033[m {string.__repr__()}')
    tokens_list = lexer.lexical_analysis(string)
    print('\033[34mRaw Token list:\033[m')
    pprint.pprint(tokens_list, width=1)
    print('\033[34mSyntax Tree:\033[m')
    generate_syntax_tree(tokens_list)

