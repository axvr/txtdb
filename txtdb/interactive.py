"""Interact with the database using a SQL REPL"""

import readline
from os import getcwd
from os.path import isfile, join, expanduser
from txtql.tokenizer import Tokenizer
from txtql.parser import Parser
from txtql.generator import Generator

# TODO add support for writing queries across multiple lines

def interactive_sql():
    """Start the SQL REPL"""

    # TODO Maybe put this in ~/.config instead
    history_file = join(expanduser("~"), ".txtdb_history")

    if not isfile(history_file):
        open(history_file, 'a').close()

    readline.read_history_file(history_file)

    try:
        while True:
            cmd = input("> ")

            if cmd.lower().strip() == "quit": break

            try:
                tokens = Tokenizer(cmd).tokenize()

                trees = Parser(tokens).parse()

                if trees is not None and len(trees) > 0:
                    for tree in trees:
                        print(tree) # NOTE: Temporary

                        generated_code = Generator().generate(trees)
                        # TODO execute generated code
                        # TODO print number of affected lines

            except RuntimeError as error:
                print(error.args[-1])

    except KeyboardInterrupt:
        print()
        interactive_sql()

    except EOFError:
        print()
        return

    finally:
        readline.write_history_file(history_file)
