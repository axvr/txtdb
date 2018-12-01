from database import Database
from cli import parse_cli_options

def main():
    (opt, args) = parse_cli_options()
    db = Database(opt.database)

    # Examples
    # --------

    # Insert a record into a table
    db.tables["example"].insert(["8a58bf89-6c64-42c9-9ab8-a39bf01e4b4f", "Fred", False, 12])

    # Update a row
    db.tables["example"].update(
            ["8a58bf89-6c64-42c9-9ab8-a39bf01e4b4f", "Fred", False, 12],
            ["8a58bf89-6c64-42c9-9ab8-a39bf01e4b4f", "Fred", True,  85])

    # Delete a row from a table
    db.tables["example"].delete(["8a58bf89-6c64-42c9-9ab8-a39bf01e4b4f", "Fred", True, 85])

    # Create a new table
    db.create_table("something", [{"name": "test", "nullable": False, "primary key": True, "type": str}])
    db.tables["something"].insert(["Hello, World!"])

    # Drop a table from the database
    db.drop("something")

    # Write the contents of the database to disk
    db.write()

    db.create_backup()

# TODO interactive mode, to import CSV files
# TODO interactive SQL environment (use recursive interface?)
