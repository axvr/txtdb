import readline

from os import getcwd
from os.path import isfile, join, expanduser
from distutils.dir_util import mkpath

from txtql.tokeniser import Tokeniser
from txtql.parser import Parser
from txtql.generator import Generator

# TODO add support for writing queries across multiple lines

def sql_interactive(db):
    """Start the SQL REPL"""

    history_dir =  join(expanduser("~"), ".config", "txtdb")
    history_file = join(history_dir, "history")

    if not isfile(history_file):
        mkpath(history_dir)
        open(history_file, "a").close()

    readline.read_history_file(history_file)

    try:
        while True:
            cmd = input("> ")

            if cmd.lower().strip() == "quit": break

            try:
                tokens = Tokeniser(cmd).tokenise()

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


def sql_file(filepath, db):
    """Execute a SQL file on the Database"""
    fh = open(filepath, "r")

    # Remove all trailing and leading whitespace on tokens
    code = " ".join(map(lambda x: x.strip(), fh.readlines()))
    fh.close()

    print("== Tokens ==\n")
    tokens = Tokeniser(code).tokenise()
    print(tokens)

    print("\n== Trees ==\n")
    trees = Parser(tokens).parse()
    for tree in trees:
        print(tree)

    print("\n== Generated Code ==\n")
    generated_code = Generator().generate(tree)
    print(generated_code)

    # TODO execute generated code on the database
    # TODO print number of affected lines
