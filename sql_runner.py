import readline

from os.path import isfile, join

from txtql.tokeniser import Tokeniser
from txtql.parser import Parser
from txtql.generator import Generator

def sql_repl(db):
    """Start the SQL REPL"""

    HISTORY_FILE = join(db.database_dir, ".repl_hist")

    if not isfile(HISTORY_FILE):
        open(HISTORY_FILE, "a").close()

    readline.read_history_file(HISTORY_FILE)

    try:
        while True:
            cmd = input("> ")

            # TODO add support for writing queries across multiple lines

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
        sql_repl(db)

    except EOFError:
        print()
        return

    finally:
        readline.write_history_file(HISTORY_FILE)


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
