"""CLI tools for txtdb"""

import argparse

def parse_args():
    """Parse the CLI arguments"""

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--database",
            dest="database", default="example",
            help="Path to the database directory")

    parser.add_argument("-i", "--interactive",
            dest="interactive", action="store_true",
            help="Interactive SQL session")

    parser.add_argument("-f", "--file",
            dest="sql_file", default=None,
            help="SQL file to execute on the database")

    parser.add_argument("--force",
            dest="ignore_lock", action="store_true",
            help="Ignore the database lock file (dangerous)")

    return parser.parse_args()
