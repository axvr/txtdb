import argparse

def parse_cli_options():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--database", dest="database", default="example",
            help="Specifiy the path to the database directory")

    parser.add_argument("-i", "--interactive", dest="interactive",
            action="store_true", help="Interactive SQL session")

    parser.add_argument("-f", "--file", dest="sql_file",
            default=None, help="SQL file to execute on the database")

    return parser.parse_args()
