import argparse

def parse_cli_options():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--database", dest="database", default="example",
            help="Specifiy the path to the database directory")

    parser.add_argument("-i", "--interactive", dest="interactive",
            action="store_true", help="Interactive SQL session")

    return parser.parse_args()
