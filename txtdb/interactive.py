"""Interact with the database using a SQL REPL"""

import readline
from txtql.tokenizer import Tokenizer
from txtql.parser import Parser
from txtql.generator import Generator

def interactive_sql():
    """Start the SQL REPL"""
    try:
        while True:
            cmd = input("> ")

            if cmd.lower() == "quit": break
            if cmd.lower().strip() == "": continue

            try:
                tokens = Tokenizer(cmd).tokenize()
                tree = Parser(tokens).parse()[0]

                print(tree) # NOTE: Temporary

                generated_code = Generator().generate(tree)
            except RuntimeError as error:
                print(error.args[-1])

            # TODO execute generated code

            # TODO print number of affected lines

    except KeyboardInterrupt:
        print()
        interactive_sql()

    except EOFError:
        print()
        return
