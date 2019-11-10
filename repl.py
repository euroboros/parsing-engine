#!/usr/bin/env python3
"""Tulip REPL

A simple program that interfaces with the lexer to make an interactive Command Line Interface."""

def main():
    """The actual REPL program. If run, shows a prompt to get input and then parses it."""

    # Import useful modules
    import lexer

    try:
        while True:
            input_ = input('repl> ')
            a = lexer.lexical_analysis(input_)
            print(a)
            tree = lexer.generate_syntax_tree(a)
    except KeyboardInterrupt:
        print('\nREPL finished.')

if __name__ == '__main__':
    # Start the REPL if running it as a file.
    main()
