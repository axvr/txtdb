from distutils.dir_util import mkpath

from database import Database
from cli import parse_cli_options
import sql_runner

def main():
    args = parse_cli_options()

    # Create the database if it doesn't already exist
    mkpath(args.database) # TODO maybe remove this
    db = Database(args.database)

    # Execute a SQL file
    if args.sql_file:
        sql_runner.sql_file(args.sql_file, db)

    # SQL REPL
    if args.interactive:
        sql_runner.sql_repl(db)

    # TODO maybe accept SQL input through STDIN

    return

# TODO to import CSV files (interactively)
