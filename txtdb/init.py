from optparse import OptionParser
from helpers import get_table_list
from database import Database

def main():
    (opt, args) = parse_cli_options()
    db = Database(opt.database)

def parse_cli_options():
    """https://docs.python.org/3.1/library/optparse.html#module-optparse"""
    parser = OptionParser()
    parser.add_option("-d", "--database", dest="database", default="example",
            help="Specifiy the path to the database directory")
    return parser.parse_args()

# TODO interactive mode, to import CSV files
