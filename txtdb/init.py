from optparse import OptionParser
from database import Database

def main():
    (opt, args) = parse_cli_options()
    db = Database(opt.database)

    # Examples
    # --------

    # Insert a record into a table
    # db.tables["example"].insert(["8a58bf89-6c64-42c9-9ab8-a39bf01e4b4f", "Fred", False, 12])

    # Create a new table
    db.create_table("something", [{"name": "test", "nullable": False, "primary key": True, "type": str}])
    db.tables["something"].insert(["Hello, World!"])

    # Drop a table from the database
    db.drop("something")

    # Write the contents of the database to disk
    db.write()

def parse_cli_options():
    parser = OptionParser()
    parser.add_option("-d", "--database", dest="database", default="example",
            help="Specifiy the path to the database directory")
    return parser.parse_args()

# TODO interactive mode, to import CSV files
# TODO interactive SQL environment (use recursive interface?)
