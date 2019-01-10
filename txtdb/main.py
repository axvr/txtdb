from database import Database
from cli import parse_cli_options

def main():
    args = parse_cli_options()
    db = Database(args.database)

    # SQL REPL
    if args.interactive:
        interactive_sql()

    return

# TODO interactive mode, to import CSV files
