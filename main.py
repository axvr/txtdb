from distutils.dir_util import mkpath

from txtng.database import Database
import cli
import sql_runner

def main():
    args = cli.parse_args()

    # Create the database if it doesn't already exist
    mkpath(args.database)

    # Instantiate the requested database instance
    db = Database(args.database, args.ignore_lock)

    # Execute a SQL file
    if args.sql_file:
        sql_runner.sql_file(args.sql_file, db)

    # SQL REPL
    if args.interactive:
        sql_runner.sql_repl(db)

    # TODO maybe accept SQL input through STDIN

    return

# TODO to import CSV files (interactively)
