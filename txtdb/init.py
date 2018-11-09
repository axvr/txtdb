from optparse import OptionParser
from helpers import get_table_list
from reader import Reader

def main():
    parse_cli_options()
    for i in get_table_list("database"):
        print(i)

def parse_cli_options():
    """https://docs.python.org/3.1/library/optparse.html#module-optparse"""
    parser = OptionParser()
    parser.parse_args()
