from database import Database
from cli import parse_cli_options
import sql_runner

def main():
    args = parse_cli_options()
    db = Database(args.database)

    # SQL REPL
    if args.interactive:
        sql_runner.sql_interactive(db)

    # Execute a SQL file
    if args.sql_file:
        sql_runner.sql_file(args.sql_file, db)

    return

# TODO to import CSV files (interactively)
